"""
Migration des données SQLite -> PostgreSQL.

Copie le contenu de l'ancienne base fichier vers la nouvelle base PostgreSQL,
en convertissant les types que SQLite stocke de façon permissive (booléens
0/1, dates en texte) vers les types stricts attendus par PostgreSQL.

Le schéma cible doit déjà exister (il est créé par init_db()).

Usage :
    python scripts/migrate_sqlite_to_postgres.py \
        --sqlite data/minorshield.db \
        --postgres "postgresql+psycopg2://user:pass@host:5432/minorshield"

Options :
    --dry-run   n'écrit rien, affiche seulement ce qui serait migré
    --truncate  vide les tables cibles avant l'import (relance propre)

La base SQLite n'est jamais modifiée : elle est ouverte en lecture seule.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine

# Ordre d'insertion : les tables référencées d'abord (clés étrangères).
TABLE_ORDER = ["parents", "children", "detections", "subscriptions"]

# Colonnes booléennes : SQLite les stocke en 0/1, PostgreSQL exige true/false.
BOOLEAN_COLUMNS = {
    "parents":       {"notif_on_detection", "notif_daily_summary", "email_verified"},
    "children":      {"is_active", "is_locked", "protection_active",
                      "capture_active", "overlay_allowed", "usage_access"},
    "subscriptions": {"is_active"},
    "detections":    set(),
}

# Colonnes de date : SQLite les stocke souvent en texte.
DATETIME_COLUMNS = {
    "parents":       {"created_at", "verification_expires_at"},
    "children":      {"pairing_expires_at", "created_at", "last_seen_at", "paired_at"},
    "detections":    {"timestamp"},
    "subscriptions": {"expires_at", "created_at", "updated_at"},
}

_DATE_FORMATS = (
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d",
)


def to_bool(value):
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).strip().lower() in {"1", "true", "t", "yes", "y"}


def to_datetime(value):
    if value is None or isinstance(value, datetime):
        return value
    text_value = str(value).strip()
    if not text_value:
        return None
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(text_value, fmt)
        except ValueError:
            continue
    print(f"    ! date non reconnue, ignorée : {text_value!r}")
    return None


def convert_row(table: str, row: dict) -> dict:
    bools = BOOLEAN_COLUMNS.get(table, set())
    dates = DATETIME_COLUMNS.get(table, set())
    out = {}
    for key, value in row.items():
        if key in bools:
            out[key] = to_bool(value)
        elif key in dates:
            out[key] = to_datetime(value)
        else:
            out[key] = value
    return out


def common_columns(src: Engine, dst: Engine, table: str) -> list[str]:
    """Colonnes présentes des deux côtés (on ignore les écarts éventuels)."""
    src_cols = [c["name"] for c in inspect(src).get_columns(table)]
    dst_cols = {c["name"] for c in inspect(dst).get_columns(table)}
    kept = [c for c in src_cols if c in dst_cols]
    for missing in set(src_cols) - dst_cols:
        print(f"    ! colonne absente de la cible, ignorée : {table}.{missing}")
    return kept


def migrate_table(src: Engine, dst: Engine, table: str, dry_run: bool) -> int:
    columns = common_columns(src, dst, table)
    if not columns:
        print(f"  {table} : aucune colonne commune, ignorée")
        return 0

    with src.connect() as sconn:
        rows = [dict(r._mapping) for r in sconn.execute(text(f"SELECT * FROM {table}"))]

    if not rows:
        print(f"  {table} : 0 ligne")
        return 0

    payload = [convert_row(table, {c: r.get(c) for c in columns}) for r in rows]

    if dry_run:
        print(f"  {table} : {len(payload)} ligne(s) — simulation, rien écrit")
        return len(payload)

    col_list = ", ".join(columns)
    val_list = ", ".join(f":{c}" for c in columns)
    stmt = text(f"INSERT INTO {table} ({col_list}) VALUES ({val_list})")

    inserted = 0
    with dst.begin() as dconn:
        for row in payload:
            try:
                dconn.execute(stmt, row)
                inserted += 1
            except Exception as exc:
                pk = row.get("id", "?")
                print(f"    ! échec sur {table}.id={pk} : {str(exc)[:120]}")
    print(f"  {table} : {inserted}/{len(payload)} ligne(s) migrée(s)")
    return inserted


def reset_sequences(dst: Engine) -> None:
    """Recale les séquences des colonnes auto-incrémentées après import."""
    query = text("""
        SELECT table_name, column_name, pg_get_serial_sequence(table_name, column_name) AS seq
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND pg_get_serial_sequence(table_name, column_name) IS NOT NULL
    """)
    with dst.begin() as conn:
        for table, column, seq in conn.execute(query):
            conn.execute(text(
                f"SELECT setval('{seq}', COALESCE((SELECT MAX({column}) FROM {table}), 1))"
            ))
            print(f"  séquence recalée : {table}.{column}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Migration SQLite -> PostgreSQL")
    ap.add_argument("--sqlite", default="data/minorshield.db")
    ap.add_argument("--postgres", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--truncate", action="store_true")
    args = ap.parse_args()

    src = create_engine(f"sqlite:///{args.sqlite}")
    dst = create_engine(args.postgres)

    print(f"Source : {args.sqlite}")
    print(f"Cible  : {args.postgres.split('@')[-1]}")
    print("Mode   :", "SIMULATION (aucune écriture)" if args.dry_run else "MIGRATION RÉELLE")
    print()

    src_tables = set(inspect(src).get_table_names())
    dst_tables = set(inspect(dst).get_table_names())
    tables = [t for t in TABLE_ORDER if t in src_tables and t in dst_tables]

    missing = [t for t in TABLE_ORDER if t in src_tables and t not in dst_tables]
    if missing:
        print(f"ERREUR : tables absentes de la cible : {', '.join(missing)}")
        print("Lancez d'abord l'application une fois pour créer le schéma.")
        return 1

    if args.truncate and not args.dry_run:
        print("Vidage des tables cibles…")
        with dst.begin() as conn:
            conn.execute(text(f"TRUNCATE {', '.join(tables)} RESTART IDENTITY CASCADE"))
        print()

    print("Migration des données :")
    total = sum(migrate_table(src, dst, t, args.dry_run) for t in tables)

    if not args.dry_run:
        print("\nRecalage des séquences :")
        reset_sequences(dst)

        print("\nVérification (source -> cible) :")
        ok = True
        for t in tables:
            with src.connect() as sc:
                n_src = sc.execute(text(f"SELECT COUNT(*) FROM {t}")).scalar()
            with dst.connect() as dc:
                n_dst = dc.execute(text(f"SELECT COUNT(*) FROM {t}")).scalar()
            flag = "OK" if n_src == n_dst else "ÉCART"
            if n_src != n_dst:
                ok = False
            print(f"  {t:<15} {n_src:>6} -> {n_dst:<6} {flag}")
        print("\n" + ("Migration terminée avec succès." if ok
                      else "Migration terminée AVEC DES ÉCARTS — à vérifier."))
        return 0 if ok else 2

    print(f"\nSimulation terminée : {total} ligne(s) seraient migrées.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
