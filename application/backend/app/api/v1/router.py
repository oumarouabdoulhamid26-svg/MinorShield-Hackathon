# app/api/v1/router.py
# Regroupe tous les endpoints de la version 1 de l'API.
#
# Le préfixe /api/v1 est ajouté automatiquement à tous les endpoints.
# Ainsi :
#   /health  devient  /api/v1/health
#   /detect  devient  /api/v1/detect
#
# Si demain on crée une version 2, on crée simplement
# un dossier v2/ avec un nouveau router — sans toucher à v1.
# Les anciens clients Android continuent de fonctionner sur v1.

from fastapi import APIRouter
from app.api.v1.endpoints import health, detection, auth, children, payment

router = APIRouter(prefix="/api/v1")

router.include_router(health.router,     tags=["Santé"])
router.include_router(detection.router,  tags=["Détection"])
router.include_router(auth.router)
router.include_router(children.router)
router.include_router(payment.router)