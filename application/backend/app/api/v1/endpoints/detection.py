# app/api/v1/endpoints/detection.py
# Endpoint principal de détection — version complète.
#
# Maintenant branché sur :
#   - OCRService (extraction texte)
#   - ImageDetectionService (NudeNet)
#   - TextDetectionService (OpenAI)
#   - DetectionService (orchestration parallèle)

import io
import uuid
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile, Depends, Request
from loguru import logger
from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session

from app.core.limiter import limiter
from app.core.config import settings
from app.core.security import verify_api_key
from app.core.database import get_db
from app.core.exceptions import (
    InvalidMediaTypeException,
    ImageTooLargeException,
    ImageCorruptedException,
    ImageDimensionsTooLargeException
)
from app.schemas.response import DetectionResponse
from app.services.detection_service import detection_service
from app.services.history_service import save_detection
from app.models.db_models import Child, Subscription
from datetime import datetime

router = APIRouter()


def validate_image_bytes(image_bytes: bytes) -> None:
    try:
        with Image.open(io.BytesIO(image_bytes)) as uploaded_image:
            uploaded_image.verify()

        with Image.open(io.BytesIO(image_bytes)) as uploaded_image:
            image_format = uploaded_image.format
            width, height = uploaded_image.size
    except (UnidentifiedImageError, OSError):
        raise ImageCorruptedException()

    if image_format not in settings.ALLOWED_IMAGE_FORMATS:
        raise InvalidMediaTypeException(image_format or "unknown")

    if (
        width > settings.MAX_IMAGE_WIDTH
        or height > settings.MAX_IMAGE_HEIGHT
        or width * height > settings.MAX_IMAGE_PIXELS
    ):
        raise ImageDimensionsTooLargeException(width, height)


@router.post(
    "/detect",
    response_model = DetectionResponse,
    summary        = "Analyser une capture d'écran",
    description    = "Reçoit une image depuis l'Android, l'analyse avec l'IA et retourne un score NSFW",
    tags           = ["Détection"]
)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def detect_content(
    request     : Request,
    image       : UploadFile        = File(..., description="Capture d'écran (JPEG, PNG, WEBP)"),
    child_id    : Optional[str]     = Form(None, description="Identifiant de l'enfant (appairage)"),
    app_package : Optional[str]     = Form(None, description="Package de l'app en premier plan"),
    app_name    : Optional[str]     = Form(None, description="Nom lisible de l'app en premier plan"),
    api_key     : str               = Depends(verify_api_key),
    db          : Session           = Depends(get_db),
) -> DetectionResponse:
    """
    Pipeline complet d'analyse :
    1. Validation du fichier
    2. OCR + Analyse image + Analyse texte (en parallèle)
    3. Score combiné
    4. Décision finale
    5. Suppression immédiate de l'image
    """

    # ── Identifiant unique pour cette requête ─────────────────────
    request_id = str(uuid.uuid4())
    logger.info(f"[{request_id}] Nouvelle requête reçue")

    # ── Étape 1 : Validation du type de fichier ───────────────────
    if image.content_type not in settings.ALLOWED_MIME_TYPES:
        logger.warning(
            f"[{request_id}] Type refusé : {image.content_type}"
        )
        raise InvalidMediaTypeException(image.content_type)

    # ── Étape 2 : Lecture des bytes ───────────────────────────────
    try:
        image_bytes = await image.read()
    except Exception:
        raise ImageCorruptedException()

    # ── Étape 3 : Validation de la taille ────────────────────────
    size_mb = len(image_bytes) / (1024 * 1024)
    if len(image_bytes) > settings.MAX_IMAGE_SIZE_BYTES:
        logger.warning(
            f"[{request_id}] Image trop grande : {size_mb:.1f} Mo"
        )
        raise ImageTooLargeException(size_mb)

    validate_image_bytes(image_bytes)

    logger.info(
        f"[{request_id}] Image reçue : "
        f"{image.filename} ({size_mb:.2f} Mo)"
    )

    # ── Étape 4 : Enfant, abonnement et réglages personnalisés ───
    child = db.query(Child).filter(Child.id == child_id).first() if child_id else None

    if not settings.SUBSCRIPTION_ENFORCED:
        # Mode test : toutes les fonctionnalités actives sans abonnement.
        analyze_images = True
        logger.info(f"[{request_id}] Paywall désactivé → analyse complète")
    else:
        analyze_images = False
        if child:
            sub = db.query(Subscription).filter(
                Subscription.parent_id == child.parent_id,
                Subscription.is_active == True,
            ).first()
            if sub and (sub.expires_at is None or sub.expires_at > datetime.utcnow()):
                analyze_images = True
        if not analyze_images:
            logger.info(f"[{request_id}] Plan gratuit → texte uniquement (images non analysées)")

    # Réglages PAR ENFANT : intensité de blocage (→ seuil) + mots sensibles perso.
    from app.services.children_service import intensity_threshold
    threshold = intensity_threshold(child.block_intensity) if child else None
    extra_keywords = None
    if child and child.custom_keywords:
        extra_keywords = [
            k.strip()
            for k in child.custom_keywords.replace(",", "\n").splitlines()
            if k.strip()
        ]

    # ── Étape 5 : Analyse via DetectionService ────────────────────
    result = await detection_service.analyze(
        image_bytes    = image_bytes,
        request_id     = request_id,
        threshold      = threshold,
        analyze_images = analyze_images,
        extra_keywords = extra_keywords,
    )

    # ── Étape 6 : Suppression immédiate (confidentialité) ─────────
    del image_bytes  # Image JAMAIS stockée

    # ── Étape 7 : Sauvegarde en base si child_id fourni ──────────
    # On ne persiste QUE le contenu inapproprié (label == "nsfw") : le contenu
    # sain n'a pas à être comptabilisé ni conservé (confidentialité + les
    # compteurs affichés au parent ne doivent refléter que les incidents réels).
    if child_id and result.label == "nsfw":
        try:
            save_detection(
                db           = db,
                child_id     = child_id,
                request_id   = result.request_id,
                nsfw_score   = result.nsfw_score,
                image_score  = result.image_score,
                text_score   = result.text_score,
                label        = result.label,
                category     = result.category,
                extracted_text = result.extracted_text,
                app_package  = app_package,
                app_name     = app_name,
            )
            # Alerte push au parent (best-effort, non bloquant).
            from app.services.notification_service import notify_parent_of_detection
            notify_parent_of_detection(db, child_id, result.category)
        except Exception as e:
            logger.warning(f"[{request_id}] Impossible de sauvegarder la détection : {e}")

    # ── Étape 7 : Retour du résultat à l'Android ──────────────────
    return DetectionResponse(
        request_id     = result.request_id,
        nsfw_score     = result.nsfw_score,
        label          = result.label,
        category       = result.category,
        image_score    = result.image_score,
        text_score     = result.text_score,
        extracted_text = result.extracted_text,
        processing_ms  = result.processing_ms,
        timestamp      = result.timestamp
    )
