
# app/core/database.py
# Base de données SQLite via SQLAlchemy.
# Stocke : comptes parents, enfants appairés, historique détections.

import os

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings

# Configurable via DATABASE_URL dans .env pour une base PERSISTANTE en
# production (ex. volume monté sur /data → DATABASE_URL=sqlite:////data/minorshield.db).
# Par défaut : app/core/../../data/minorshield.db (dossier data/ à la racine de Server/).
DATABASE_URL = settings.DATABASE_URL
_FALLBACK_URL = "sqlite:///./data/minorshield.db"


def _ensure_sqlite_writable(url: str) -> str:
    """
    Garantit que l'emplacement du fichier SQLite est accessible en écriture.
    Si ce n'est pas le cas (ex: volume Railway mal monté sur /data), on
    BASCULE sur un fichier local plutôt que de laisser l'app planter au
    démarrage — la disponibilité prime, surtout en démo.
    """
    if not url.startswith("sqlite:///"):
        return url
    path = url[len("sqlite:///"):]
    directory = os.path.dirname(path) or "."
    try:
        os.makedirs(directory, exist_ok=True)
        probe = os.path.join(directory, ".write_test")
        with open(probe, "w"):
            pass
        os.remove(probe)
        return url
    except Exception as e:
        logger.warning(
            f"Base : emplacement '{directory}' inaccessible en écriture ({e}) "
            f"→ bascule sur {_FALLBACK_URL}"
        )
        return _FALLBACK_URL


IS_SQLITE = DATABASE_URL.startswith("sqlite")

# Le contrôle d'écriture ne concerne que SQLite (base = fichier local).
if IS_SQLITE:
    DATABASE_URL = _ensure_sqlite_writable(DATABASE_URL)

if IS_SQLITE:
    # check_same_thread : spécifique au driver SQLite.
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # PostgreSQL : pool de connexions avec pre-ping, pour survivre aux coupures
    # réseau et aux connexions fermées par le serveur après inactivité.
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        pool_recycle=1800,
    )

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Colonnes ajoutées après la création initiale du schéma.
# (nom_table, nom_colonne, type SQLite, type PostgreSQL)
# Les types diffèrent : SQLite tolère DATETIME/DEFAULT 0 pour un booléen,
# PostgreSQL exige TIMESTAMP et de vrais true/false.
_PROGRESSIVE_COLUMNS = [
    ("children", "is_locked",          "BOOLEAN DEFAULT FALSE",   "BOOLEAN DEFAULT false"),
    ("children", "protection_active",  "BOOLEAN DEFAULT 0",       "BOOLEAN DEFAULT false"),
    ("children", "last_seen_at",       "DATETIME",                "TIMESTAMP"),
    ("children", "age",                "INTEGER",                 "INTEGER"),
    ("children", "device_model",       "VARCHAR",                 "VARCHAR"),
    ("children", "paired_at",          "DATETIME",                "TIMESTAMP"),
    ("children", "capture_active",     "BOOLEAN DEFAULT 0",       "BOOLEAN DEFAULT false"),
    ("children", "overlay_allowed",    "BOOLEAN DEFAULT 0",       "BOOLEAN DEFAULT false"),
    ("children", "usage_access",       "BOOLEAN DEFAULT 0",       "BOOLEAN DEFAULT false"),
    ("children", "warning_limit",      "INTEGER DEFAULT 3",       "INTEGER DEFAULT 3"),
    ("children", "warnings_used",      "INTEGER DEFAULT 0",       "INTEGER DEFAULT 0"),
    ("children", "warnings_reset_day", "VARCHAR",                 "VARCHAR"),
    ("children", "custom_keywords",    "TEXT",                    "TEXT"),
    ("children", "block_intensity",    "VARCHAR DEFAULT 'eleve'", "VARCHAR DEFAULT 'eleve'"),
    ("detections", "category",         "VARCHAR",                 "VARCHAR"),
    ("detections", "app_name",         "VARCHAR",                 "VARCHAR"),
    ("parents", "pin_hash",            "VARCHAR",                 "VARCHAR"),
    ("parents", "notif_on_detection",  "BOOLEAN DEFAULT 1",       "BOOLEAN DEFAULT true"),
    ("parents", "notif_daily_summary", "BOOLEAN DEFAULT 1",       "BOOLEAN DEFAULT true"),
    ("parents", "name",                "VARCHAR",                 "VARCHAR"),
    ("parents", "email_verified",      "BOOLEAN DEFAULT 0",       "BOOLEAN DEFAULT false"),
    ("parents", "verification_code",   "VARCHAR",                 "VARCHAR"),
    ("parents", "verification_expires_at", "DATETIME",            "TIMESTAMP"),
]


def init_db():
    from app.models.db_models import Parent, Child, Detection, Subscription  # noqa: F401
    from sqlalchemy import text, inspect

    Base.metadata.create_all(bind=engine)

    # Migrations progressives : on n'ajoute que les colonnes réellement
    # manquantes (plutôt que d'exécuter à l'aveugle en avalant l'erreur).
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    for table, column, sqlite_type, pg_type in _PROGRESSIVE_COLUMNS:
        if table not in existing_tables:
            continue
        columns = {c["name"] for c in inspector.get_columns(table)}
        if column in columns:
            continue
        col_type = sqlite_type if IS_SQLITE else pg_type
        try:
            with engine.connect() as conn:
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}"))
                conn.commit()
            logger.info(f"Base : colonne ajoutée {table}.{column}")
        except Exception as e:
            logger.warning(f"Base : ajout de {table}.{column} impossible ({e})")
