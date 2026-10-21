# app/services/detection_service.py
# Service principal d'orchestration de la détection.
#
# C'est le chef d'orchestre qui coordonne :
#   1. L'extraction de texte (OCR)
#   2. L'analyse visuelle (NudeNet)
#   3. L'analyse textuelle (OpenAI)
#   4. La combinaison des scores
#
# La grande force de ce service : les analyses image
# et texte sont lancées EN PARALLÈLE grâce à asyncio.
# Résultat : temps de traitement divisé par 2.

import asyncio
import uuid
from datetime import datetime
from loguru import logger

from app.core.config import settings
from app.services.ocr_service import ocr_service
from app.services.image_service import image_detection_service
from app.services.violence_service import violence_detection_service
from app.services.text_service import text_detection_service


class DetectionResult:
    """
    Résultat complet d'une analyse de capture d'écran.
    Contient tous les scores et la décision finale.
    """
    def __init__(
        self,
        request_id     : str,
        nsfw_score     : float,
        label          : str,
        category       : str,
        image_score    : float,
        text_score     : float,
        extracted_text : str,
        processing_ms  : int,
        timestamp      : str
    ):
        self.request_id     = request_id
        self.nsfw_score     = nsfw_score
        self.label          = label
        self.category       = category
        self.image_score    = image_score
        self.text_score     = text_score
        self.extracted_text = extracted_text
        self.processing_ms  = processing_ms
        self.timestamp      = timestamp


class DetectionService:
    """
    Orchestre l'analyse complète d'une capture d'écran.

    Pipeline d'analyse :

    image_bytes
         │
         ├──────────────────────────────────┐
         │                                  │
         ▼                                  ▼
    OCR (extraction texte)          Analyse image (NudeNet)
         │                                  │
         ▼                                  │
    Analyse texte (OpenAI)                  │
         │                                  │
         └──────────────┬───────────────────┘
                        │
                        ▼
              Score combiné final
              (image×60% + texte×40%)
                        │
                        ▼
                  Décision finale
                (safe ou nsfw)
    """

    async def analyze(
        self,
        image_bytes    : bytes,
        request_id     : str   = None,
        threshold      : float = None,
        analyze_images : bool  = True,
        extra_keywords : list  = None,
    ) -> DetectionResult:
        """
        Analyse complète d'une capture d'écran.

        Args:
            image_bytes : Bytes de l'image à analyser
            request_id  : Identifiant unique de la requête
            threshold   : Seuil de détection (défaut : config)

        Returns:
            DetectionResult : Résultat complet avec tous les scores
        """
        import time
        start_time = time.time()

        if request_id is None:
            request_id = str(uuid.uuid4())

        if threshold is None:
            threshold = settings.DEFAULT_THRESHOLD

        logger.info(f"[{request_id}] Début analyse parallèle...")
        loop = asyncio.get_event_loop()

        # OCR + analyse texte enchaînés dans une seule coroutine, pour les faire
        # tourner EN PARALLÈLE de l'analyse d'image. Avant, l'OCR (lent sur CPU)
        # s'exécutait SEUL en premier et bloquait tout → grosse latence.
        async def _ocr_then_text():
            txt = await loop.run_in_executor(None, ocr_service.extract_text, image_bytes)
            sc  = await loop.run_in_executor(None, text_detection_service.analyze, txt, extra_keywords)
            return txt, sc

        # ── Analyses en parallèle ─────────────────────────────────
        if analyze_images:
            # Abonné : (OCR→texte) ‖ nudité ‖ violence visuelle
            (extracted_text, text_score), nudity_score, violence_score = await asyncio.gather(
                _ocr_then_text(),
                loop.run_in_executor(None, image_detection_service.analyze, image_bytes),
                loop.run_in_executor(None, violence_detection_service.analyze, image_bytes),
            )
            image_score = round(max(nudity_score, violence_score), 4)
        else:
            # Gratuit : texte uniquement (pas d'analyse visuelle)
            extracted_text, text_score = await _ocr_then_text()
            nudity_score   = 0.0
            violence_score = 0.0
            image_score    = 0.0
            logger.info(f"[{request_id}] Mode gratuit — analyse texte uniquement")

        logger.debug(
            f"[{request_id}] Analyses terminées → "
            f"image={image_score:.3f}, texte={text_score:.3f}"
        )

        # ── Étape 3 : Calcul du score combiné ────────────────────
        nsfw_score = (
            image_score * settings.WEIGHT_IMAGE +
            text_score  * settings.WEIGHT_TEXT
        )
        nsfw_score = round(min(nsfw_score, 1.0), 4)

        # ── Étape 4 : Décision finale intelligente ────────────────────
        # Règle 1 : Score combiné dépasse le seuil global
        if nsfw_score >= threshold:
            label = "nsfw"

        # Règle 2 : Image seule très suspecte (abonnés uniquement)
        elif analyze_images and image_score >= 0.50:
            label      = "nsfw"
            nsfw_score = max(nsfw_score, image_score)

        # Règle 3 : Texte seul très suspect → bloquer directement
        elif text_score >= 0.80:
            label      = "nsfw"
            nsfw_score = max(nsfw_score, text_score)

        else:
            label = "safe"

        # ── Étape 4bis : Catégorie dominante (raison du blocage) ──
        # Indique au parent QUEL signal a déclenché le blocage :
        # nudité, violence visuelle (sang/bagarre/accident) ou texte.
        if label == "nsfw":
            category = max(
                ("nudite", nudity_score),
                ("violence", violence_score),
                ("texte", text_score),
                key=lambda pair: pair[1],
            )[0]
        else:
            category = None

        # ── Étape 5 : Temps de traitement ─────────────────────────
        processing_ms = int((time.time() - start_time) * 1000)

        logger.info(
            f"[{request_id}] ✅ Analyse complète → "
            f"score={nsfw_score}, label={label}, categorie={category}, "
            f"durée={processing_ms}ms"
        )

        return DetectionResult(
            request_id     = request_id,
            nsfw_score     = nsfw_score,
            label          = label,
            category       = category,
            image_score    = image_score,
            text_score     = text_score,
            extracted_text = extracted_text if extracted_text else None,
            processing_ms  = processing_ms,
            timestamp      = datetime.utcnow().isoformat()
        )


# ── Instance globale ──────────────────────────────────────────────────
detection_service = DetectionService()