# app/services/violence_service.py
# Détection de violence visuelle (sang, bagarres, accidents, contenu graphique)
# dans les captures d'écran.
#
# NudeNet (image_service.py) ne détecte que la nudité — ce module complète
# la couverture visuelle avec l'API de modération multimodale d'OpenAI
# (gratuite, image jamais stockée, envoyée uniquement pour l'analyse).

import base64
import io

from PIL import Image
from loguru import logger
from openai import OpenAI

from app.core.config import settings


class ViolenceDetectionService:
    """
    Service de détection de violence visuelle.

    Utilise le modèle omni-moderation-latest d'OpenAI, qui accepte
    des images et retourne des scores par catégorie — dont
    "violence" et "violence/graphic" (sang, blessures, accidents).
    """

    def __init__(self):
        if settings.EXTERNAL_TEXT_ANALYSIS_ENABLED and settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            logger.info("✅ Détection violence visuelle (OpenAI) initialisée")
        else:
            self.client = None
            logger.warning("⚠️ Détection violence visuelle désactivée ou non configurée")

    def analyze(self, image_bytes: bytes) -> float:
        """
        Analyse une image et retourne un score de violence graphique.

        Args:
            image_bytes: Image brute en bytes (JPEG, PNG...)

        Returns:
            float: Score entre 0.0 (sain) et 1.0 (très violent/graphique)
                   Retourne 0.0 si le client OpenAI n'est pas configuré
        """
        if self.client is None or not settings.OPENAI_ENABLED:
            return 0.0

        try:
            data_url = self._to_data_url(image_bytes)

            response = self.client.moderations.create(
                model="omni-moderation-latest",
                input=[{"type": "image_url", "image_url": {"url": data_url}}],
            )
            scores = response.results[0].category_scores

            violence_score = max(
                scores.violence,
                scores.violence_graphic,
            )

            logger.debug(f"Analyse violence visuelle → score={violence_score:.3f}")

            return round(violence_score, 4)

        except Exception as e:
            logger.error(f"Erreur détection violence visuelle : {e}")
            return 0.0

    def _to_data_url(self, image_bytes: bytes) -> str:
        """
        Redimensionne l'image et l'encode en data URL base64.
        Rien n'est écrit sur disque, rien n'est stocké côté OpenAI.
        """
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        max_size = 768
        width, height = image.size
        if width > max_size or height > max_size:
            ratio = min(max_size / width, max_size / height)
            image = image.resize(
                (int(width * ratio), int(height * ratio)),
                Image.LANCZOS
            )

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=85)
        b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return f"data:image/jpeg;base64,{b64}"


# ── Instance globale ──────────────────────────────────────────────────
violence_detection_service = ViolenceDetectionService()
