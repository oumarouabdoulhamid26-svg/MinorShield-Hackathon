# app/api/v1/endpoints/health.py
# Endpoint de vérification du serveur.
#
# L'application Android appelle cet endpoint au démarrage
# pour confirmer que le serveur est accessible et prêt
# avant de commencer la surveillance.

from fastapi import APIRouter
from datetime import datetime
from loguru import logger

from app.core.config import settings
from app.schemas.response import HealthResponse

router = APIRouter()


def _check_models_ready() -> bool:
    """Vérifie l'état réel des modèles IA au moment de l'appel."""
    try:
        from app.services.image_service import image_detection_service
        nudenet_ok = image_detection_service.detector is not None
    except Exception:
        nudenet_ok = False

    try:
        from app.services.text_service import text_detection_service
        text_ok = (
            text_detection_service.client is not None
            or text_detection_service.hf_headers is not None
        )
    except Exception:
        text_ok = False

    return nudenet_ok and text_ok


@router.get(
    "/health",
    response_model = HealthResponse,
    summary        = "Vérification du serveur",
    description    = "Vérifie que le serveur et les modèles IA sont opérationnels",
    tags           = ["Santé"]
)
async def health_check() -> HealthResponse:
    """
    Endpoint public — pas besoin de clé API pour y accéder.

    Retourne l'état complet du serveur :
    - Est-il en ligne ?
    - Les modèles IA sont-ils chargés ?
    - Quelle version tourne ?
    - Dans quel environnement ?

    L'Android utilise cet endpoint pour :
    1. Vérifier la connexion au serveur au démarrage
    2. Afficher le statut dans l'interface parent
    3. Détecter si le serveur est tombé en cours d'utilisation
    """
    logger.info("Health check reçu")

    models_ready = _check_models_ready()

    return HealthResponse(
        status        = "ok",
        message       = "MinorShield API opérationnelle",
        version       = settings.APP_VERSION,
        environment   = settings.ENVIRONMENT,
        models_loaded = models_ready,
        timestamp     = datetime.utcnow().isoformat()
    )