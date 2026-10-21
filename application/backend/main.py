# main.py
import uvicorn
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import settings
from app.core.limiter import limiter
from app.core.exceptions import (
    MinorShieldException,
    minorshield_exception_handler
)
from app.api.v1.router import router

# ── Configuration des logs ────────────────────────────────────────────
logger.remove()
logger.add(
    sys.stdout,
    format   = (
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan> | "
        "<white>{message}</white>"
    ),
    level    = "DEBUG",
    colorize = True
)

# ── Logs persistants ──────────────────────────────────────────────────
# Les logs sont aussi sauvegardés dans un fichier
# Rotation automatique chaque jour — conservation 30 jours
logger.add(
    "logs/minorshield_{time:YYYY-MM-DD}.log",
    format      = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name} | {message}",
    level       = "INFO",
    rotation    = "00:00",
    retention   = "30 days",
    compression = "zip",
    enqueue     = True,
    mode        = "a"
)


# ── Lifespan ──────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gère le démarrage et l'arrêt du serveur.
    """
    # ── Créer le dossier logs si inexistant ───────────────────────
    import os
    os.makedirs("logs", exist_ok=True)

    # ── Démarrage ─────────────────────────────────────────────────
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} démarrée")
    logger.info(f"📡 Environnement  : {settings.ENVIRONMENT}")
    logger.info(f"🔐 Sécurité       : Authentification par clé API activée")
    logger.info(f"🚦 Rate Limiting  : {settings.RATE_LIMIT_PER_MINUTE} requêtes/minute/IP")
    if settings.ENABLE_DOCS:
        logger.info(f"Documentation  : http://localhost:{settings.PORT}/docs")
    else:
        logger.info("Documentation  : desactivee")

    from app.core.database import init_db
    init_db()
    logger.info("✅ Base de données SQLite initialisée")

    # ── Résumé quotidien (push FCM) ───────────────────────────────
    # Planificateur en arrière-plan ; dégradé proprement si apscheduler
    # n'est pas installé.
    app.state.scheduler = None
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        from app.core.database import SessionLocal
        from app.services.notification_service import send_daily_summaries

        def _daily_summary_job():
            db = SessionLocal()
            try:
                send_daily_summaries(db)
            except Exception as e:
                logger.warning(f"Résumé quotidien : échec — {e}")
            finally:
                db.close()

        scheduler = BackgroundScheduler(timezone="UTC")
        scheduler.add_job(_daily_summary_job, "cron", hour=settings.DAILY_SUMMARY_HOUR, minute=0)
        scheduler.start()
        app.state.scheduler = scheduler
        logger.info(f"✅ Résumé quotidien planifié (≈{settings.DAILY_SUMMARY_HOUR}h UTC)")
    except ImportError:
        logger.warning("Résumé quotidien désactivé — apscheduler non installé")
    except Exception as e:
        logger.warning(f"Résumé quotidien désactivé — {e}")

    from app.services.image_service import image_detection_service
    from app.services.text_service import text_detection_service

    if image_detection_service.detector is not None:
        logger.info("✅ NudeNet chargé et prêt")
    else:
        logger.warning("⚠️ NudeNet non chargé")

    if text_detection_service.client is not None:
        logger.info("✅ OpenAI Moderation API prête")
    else:
        logger.warning("⚠️ OpenAI non configuré")

    logger.info("✅ OCR Tesseract prêt")
    logger.info("✅ Logs persistants activés — dossier logs/")
    logger.info("🛡️ MinorShield est opérationnel et prêt à protéger !")

    yield

    # ── Arrêt ─────────────────────────────────────────────────────
    scheduler = getattr(app.state, "scheduler", None)
    if scheduler is not None:
        scheduler.shutdown(wait=False)
    logger.info("🛑 Serveur arrêté proprement — ressources libérées")


# ── Création de l'application ─────────────────────────────────────────
app = FastAPI(
    title       = settings.APP_NAME,
    version     = settings.APP_VERSION,
    description = """
## MinorShield API

API professionnelle de détection de contenu inapproprié
pour la protection des mineurs sur Android.

### Fonctionnalités
- 🖼️ Analyse visuelle des captures d'écran (NudeNet)
- 📝 Analyse textuelle du contenu affiché (OpenAI Moderation)
- 🔍 Extraction de texte par OCR (Tesseract)
- 🔐 Authentification par clé API
- 🚦 Rate Limiting par adresse IP
- ⚡ Analyse parallèle pour des performances optimales

### Authentification
Toutes les requêtes vers `/detect` nécessitent le header :
""",
    lifespan  = lifespan,
    docs_url  = "/docs" if settings.ENABLE_DOCS else None,
    redoc_url = "/redoc" if settings.ENABLE_DOCS else None
)

# ── Rate Limiting Middleware ──────────────────────────────────────────
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# ── Security Headers Middleware ───────────────────────────────────────
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"]    = "nosniff"
    response.headers["X-Frame-Options"]           = "DENY"
    response.headers["X-XSS-Protection"]          = "1; mode=block"
    response.headers["Referrer-Policy"]           = "no-referrer"
    response.headers["Cache-Control"]             = "no-store"
    response.headers["Permissions-Policy"]        = "camera=(), microphone=(), geolocation=()"
    if not settings.ENABLE_DOCS:
        response.headers["Content-Security-Policy"] = "default-src 'none'"
    return response

# ── CORS Middleware ───────────────────────────────────────────────────
_allow_credentials = "*" not in settings.ALLOWED_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins     = settings.ALLOWED_ORIGINS,
    allow_credentials = _allow_credentials,
    allow_methods     = ["POST", "GET"],
    allow_headers     = ["X-API-Key", "Content-Type"],
)

# ── Gestionnaire d'erreurs global ─────────────────────────────────────
app.add_exception_handler(
    MinorShieldException,
    minorshield_exception_handler
)

# ── Routes ────────────────────────────────────────────────────────────
app.include_router(router)

# ── Lancement ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host            = settings.HOST,
        port            = settings.PORT,
        reload          = True,
        # Sans ça, uvicorn surveille TOUT le dossier Server/ — y compris
        # minorshield.db et les logs, réécrits à chaque requête. Chaque écriture
        # était interprétée comme un changement de code et redémarrait le
        # serveur, coupant les requêtes en cours (ex: analyse d'image en cours).
        reload_excludes = ["*.db", "*.db-journal", "logs/*", "venv/*", "*.log"]
    )
