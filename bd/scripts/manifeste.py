"""Manifeste des sources de la base de connaissances (bd/MANIFESTE.csv).

Une ligne par document de bd/InputDocs/ : provenance (emetteur, adresse,
date de consultation), traitement, statut de verification et empreintes
SHA-256. Deux empreintes sont distinguees :
- sha256_texte    : le fichier tel qu'il est dans le depot et ingere dans la
                    base (c'est lui que les agents citent) ;
- sha256_original : le document officiel telecharge (PDF), quand un fichier
                    fige existe. Les pages web (EUR-Lex, legislation.gov.uk...)
                    n'ont pas d'original fige : la colonne reste vide.

Usage :
    python bd/scripts/manifeste.py verifier
        recalcule les empreintes des fichiers du depot et les compare au
        manifeste ; signale les fichiers modifies, manquants ou non listes,
        et les PDF tronques. Code de sortie 1 en cas d'ecart.
    python bd/scripts/manifeste.py verifier --originaux DOSSIER
        verifie aussi les documents officiels presents dans DOSSIER (par
        exemple apres les avoir retelecharges depuis la colonne source_url).
    python bd/scripts/manifeste.py mettre-a-jour [--base]
        recalcule empreintes et tailles, ajoute les nouveaux fichiers (les
        colonnes de provenance sont alors a remplir a la main) ; --base
        compte aussi les extraits de chaque fichier dans ChromaDB.

Les colonnes de provenance sont saisies a la main dans le CSV ; ce script ne
les modifie jamais.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "bd" / "InputDocs"
MANIFESTE = ROOT / "bd" / "MANIFESTE.csv"

COLONNES = [
    "fichier", "categorie", "titre", "emetteur", "pays", "langue", "source_url",
    "consulte_le", "original", "sha256_original", "octets_original",
    "traitement", "statut", "notes", "sha256_texte", "octets_texte", "extraits_base",
]

# Statuts de verification, du plus controle au moins controle.
STATUTS = {
    "integral_controle": "texte complet controle (nombre d'articles, formule de promulgation)",
    "ocr_controle_sondage": "texte obtenu par OCR d'une copie officielle, articles comptes, relu par sondage",
    "texte_officiel_extrait": "couche texte d'un document ou d'une page officielle, non relue integralement",
    "releve_manuel": "texte releve depuis la page officielle affichee (telechargement automatise refuse)",
    "fourni_uit": "document du depot de reference de l'UIT, repris tel quel",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def pdf_tronque(path: Path) -> bool:
    """Un PDF complet se termine par le marqueur %%EOF."""
    if path.suffix.lower() != ".pdf":
        return False
    with path.open("rb") as f:
        f.seek(max(0, path.stat().st_size - 2048))
        return b"%%EOF" not in f.read()


def fichiers() -> list[Path]:
    return sorted(p for p in DOCS.rglob("*") if p.is_file() and p.name != "Inputs.md")


def lire() -> dict[str, dict[str, str]]:
    if not MANIFESTE.exists():
        return {}
    with MANIFESTE.open(encoding="utf-8", newline="") as f:
        return {r["fichier"]: r for r in csv.DictReader(f)}


def ecrire(lignes: list[dict[str, str]]) -> None:
    with MANIFESTE.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLONNES, lineterminator="\n")
        w.writeheader()
        for r in lignes:
            w.writerow({c: r.get(c, "") for c in COLONNES})


def compter_extraits() -> dict[str, int]:
    sys.path.insert(0, str(ROOT))
    from bd.knowledge.kb import KnowledgeBase  # noqa: E402

    metas = KnowledgeBase().main.get(include=["metadatas"])["metadatas"]
    compte: dict[str, int] = {}
    for m in metas:
        compte[m.get("source_file", "")] = compte.get(m.get("source_file", ""), 0) + 1
    return compte


def mettre_a_jour(base: bool) -> int:
    anciens = lire()
    extraits = compter_extraits() if base else {}
    lignes, nouveaux = [], []
    for p in fichiers():
        rel = p.relative_to(DOCS).as_posix()
        r = dict(anciens.get(rel) or {"fichier": rel, "categorie": p.parent.name})
        if rel not in anciens:
            nouveaux.append(rel)
        r["sha256_texte"], r["octets_texte"] = sha256(p), str(p.stat().st_size)
        if base:
            r["extraits_base"] = str(extraits.get(p.name, 0))
        lignes.append(r)
    ecrire(lignes)
    print(f"{len(lignes)} documents dans {MANIFESTE.relative_to(ROOT).as_posix()}")
    for rel in nouveaux:
        print(f"  nouveau (provenance a completer) : {rel}")
    for rel in sorted(set(anciens) - {r['fichier'] for r in lignes}):
        print(f"  retire (fichier absent) : {rel}")
    return 0


def verifier(originaux: Path | None) -> int:
    manif = lire()
    if not manif:
        print("Manifeste absent : lancer d'abord « mettre-a-jour ».")
        return 1
    ecarts = 0
    presents = {}
    for p in fichiers():
        rel = p.relative_to(DOCS).as_posix()
        presents[rel] = p
        r = manif.get(rel)
        if r is None:
            print(f"NON LISTE  {rel}")
            ecarts += 1
        elif sha256(p) != r["sha256_texte"]:
            print(f"MODIFIE    {rel}")
            ecarts += 1
        if pdf_tronque(p):
            print(f"PDF TRONQUE (marqueur de fin absent) : {rel}")
    for rel in sorted(set(manif) - set(presents)):
        print(f"MANQUANT   {rel}")
        ecarts += 1

    sans_statut = [r["fichier"] for r in manif.values() if r["statut"] not in STATUTS]
    for rel in sans_statut:
        print(f"STATUT INCONNU ({manif[rel]['statut'] or 'vide'}) : {rel}")
    ecarts += len(sans_statut)

    verifies = 0
    if originaux:
        empreintes = {sha256(p): p for p in originaux.rglob("*") if p.is_file()}
        attendus = {r["sha256_original"]: r["original"] for r in manif.values() if r["sha256_original"]}
        for h, nom in sorted(attendus.items(), key=lambda x: x[1]):
            if h in empreintes:
                verifies += 1
                print(f"ORIGINAL OK  {nom}  ({empreintes[h].name})")
            else:
                print(f"ORIGINAL ABSENT OU DIFFERENT  {nom}")
        print(f"Originaux verifies : {verifies}/{len(attendus)}")

    print(f"{len(presents)} fichiers, {ecarts} ecart(s) avec le manifeste.")
    return 1 if ecarts else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("verifier")
    v.add_argument("--originaux", type=Path, default=None)
    m = sub.add_parser("mettre-a-jour")
    m.add_argument("--base", action="store_true")
    args = ap.parse_args()
    if args.cmd == "verifier":
        return verifier(args.originaux)
    return mettre_a_jour(args.base)


if __name__ == "__main__":
    sys.exit(main())
