from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Central application settings loaded from environment and .env."""

    APP_NAME: str = "MinorShield API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    # Connexion base de données (SQLite par défaut).
    # Le fichier vit dans data/ pour rester séparé du code source — pratique
    # pour les sauvegardes et les volumes Docker. Chemin absolu possible :
    # DATABASE_URL=sqlite:////chemin/absolu/minorshield.db
    DATABASE_URL: str = "sqlite:///./data/minorshield.db"

    API_KEY: str = ""
    ALLOWED_ORIGINS: List[str] = ["*"]
    ENABLE_DOCS: bool = True

    OPENAI_API_KEY: str = ""
    HUGGINGFACE_TOKEN: str = ""
    EXTERNAL_TEXT_ANALYSIS_ENABLED: bool = True
    # Coupe tous les appels OpenAI (modération texte + violence visuelle).
    # À mettre False quand la clé OpenAI est indisponible (429/quota) : la
    # détection texte bascule alors sur HuggingFace (gratuit).
    OPENAI_ENABLED: bool = True

    RATE_LIMIT_PER_MINUTE: int = 30

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DEFAULT_THRESHOLD: float = 0.75
    WEIGHT_IMAGE: float = 0.60
    WEIGHT_TEXT: float = 0.40
    CAPTURE_INTERVAL_MS: int = 2000

    MAX_IMAGE_SIZE_MB: int = 5
    MAX_IMAGE_SIZE_BYTES: int = 5 * 1024 * 1024
    MAX_IMAGE_WIDTH: int = 4096
    MAX_IMAGE_HEIGHT: int = 4096
    MAX_IMAGE_PIXELS: int = 12_000_000
    ALLOWED_MIME_TYPES: List[str] = [
        "image/jpeg",
        "image/png",
        "image/webp",
    ]
    ALLOWED_IMAGE_FORMATS: List[str] = [
        "JPEG",
        "PNG",
        "WEBP",
    ]

    NSFW_MODEL_PATH: str = "weights/nsfw_model"
    TEXT_MODEL_NAME: str = "unitary/multilingual-toxic-xlm-roberta"

    STORE_IMAGES: bool = False

    # Quand False : toutes les fonctionnalités (dont l'analyse d'images) sont
    # actives pour tout le monde, sans abonnement — utile pour les tests.
    # Repasser à True pour réactiver le paywall (analyse d'images = Premium).
    SUBSCRIPTION_ENFORCED: bool = False

    # JWT pour les comptes parent
    JWT_SECRET: str = "minorshield-jwt-secret-change-in-production"

    # Notifications push (Firebase Cloud Messaging).
    # Chemin du fichier JSON de compte de service Firebase (Admin SDK).
    # Si le fichier est absent, les push sont simplement désactivés (le reste
    # de l'app fonctionne). À récupérer dans la console Firebase :
    # Paramètres du projet → Comptes de service → Générer une clé privée.
    FIREBASE_CREDENTIALS_FILE: str = "firebase-service-account.json"
    # Alternative à Railway (pas de fichier committable) : coller le contenu JSON
    # du compte de service Firebase dans cette variable d'environnement.
    FIREBASE_CREDENTIALS_JSON: str = ""
    # Heure locale d'envoi du résumé quotidien (0-23).
    DAILY_SUMMARY_HOUR: int = 20

    # ── E-mail (vérification du compte) — SMTP configurable ──────────
    # Défauts Outlook ; pour Gmail : smtp.gmail.com. À remplir dans le .env :
    #   SMTP_USER = ton adresse e-mail ; SMTP_PASSWORD = mot de passe d'application.
    SMTP_HOST    : str = "smtp-mail.outlook.com"
    SMTP_PORT    : int = 587
    SMTP_USER    : str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM    : str = ""   # vide → on utilise SMTP_USER
    # Vérification e-mail RETIRÉE : elle bloquait la connexion. Désactivée par
    # défaut → les comptes sont auto-vérifiés à l'inscription (aucun code envoyé).
    EMAIL_VERIFICATION_ENABLED: bool = False

    # Monetbil
    MONETBIL_SERVICE_KEY   : str = ""   # clé publique du service (widget URL)
    MONETBIL_SERVICE_SECRET: str = ""   # secret pour vérifier les webhooks
    PUBLIC_URL             : str = "http://localhost:8081"  # URL publique du serveur

    model_config = {"env_file": ".env"}

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

    def model_post_init(self, __context) -> None:
        if self.is_production and not self.API_KEY:
            raise ValueError("API_KEY is required in production.")

        if self.is_production and "*" in self.ALLOWED_ORIGINS:
            raise ValueError("ALLOWED_ORIGINS cannot contain '*' in production.")

        if self.is_production and self.ENABLE_DOCS:
            raise ValueError("ENABLE_DOCS must be false in production.")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
