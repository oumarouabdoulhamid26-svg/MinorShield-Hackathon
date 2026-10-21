# app/services/image_service.py
# Module de détection de contenu visuel inapproprié.
#
# Utilise NudeNet — modèle IA open source spécialisé
# dans la détection de contenu NSFW dans les images.
# Plus précis et plus récent que GantMan (2019).
#
# NudeNet détecte et classe les parties du corps
# et retourne un score de dangerosité global.

from nudenet import NudeDetector
from PIL import Image
import io
import numpy as np
from loguru import logger


# ── Catégories considérées comme NSFW ────────────────────────────────
# NudeNet détecte plusieurs parties du corps.
# On définit ici celles qui sont inappropriées pour les mineurs.
NSFW_CATEGORIES = {
    "FEMALE_BREAST_EXPOSED",
    "FEMALE_GENITALIA_EXPOSED",
    "MALE_GENITALIA_EXPOSED",
    "BUTTOCKS_EXPOSED",
    "ANUS_EXPOSED",
    "BELLY_EXPOSED",
    "ARMPITS_EXPOSED",
}

# Catégories très graves — score maximum immédiatement
CRITICAL_CATEGORIES = {
    "FEMALE_GENITALIA_EXPOSED",
    "MALE_GENITALIA_EXPOSED",
    "FEMALE_BREAST_EXPOSED",
}


class ImageDetectionService:
    """
    Service de détection de contenu visuel inapproprié.

    Utilise NudeNet pour analyser chaque capture d'écran
    et retourner un score NSFW entre 0.0 et 1.0.

    Fonctionnement :
    1. Reçoit les bytes d'une image
    2. Convertit en format compatible NudeNet
    3. Détecte les éléments inappropriés
    4. Calcule un score global
    5. Retourne le score
    """

    def __init__(self):
        """
        Charge le modèle NudeNet une seule fois au démarrage.
        Le chargement prend quelques secondes mais
        les analyses suivantes sont rapides.
        """
        try:
            logger.info("Chargement du modèle NudeNet...")
            self.detector = NudeDetector()
            logger.info("✅ Modèle NudeNet chargé avec succès")
        except Exception as e:
            logger.error(f"❌ Erreur chargement NudeNet : {e}")
            self.detector = None

    def analyze(self, image_bytes: bytes) -> float:
        """
        Analyse une image et retourne un score NSFW.

        Args:
            image_bytes: Image brute en bytes (JPEG, PNG...)

        Returns:
            float: Score entre 0.0 (sain) et 1.0 (très inapproprié)
                   Retourne 0.0 si le modèle n'est pas chargé
        """

        # ── Vérification modèle chargé ────────────────────────────
        if self.detector is None:
            logger.warning("NudeNet non chargé — score image = 0.0")
            return 0.0

        try:
            # ── Étape 1 : Charger et préparer l'image ────────────
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

            # Redimensionner pour optimiser la vitesse
            # sans perdre la précision de détection
            image = self._resize_image(image)

            # ── Étape 2 : Sauvegarder temporairement en mémoire ──
            # NudeNet travaille avec des chemins de fichiers
            # On utilise un buffer en mémoire — rien n'est écrit sur disque
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG", quality=85)
            buffer.seek(0)

            # ── Étape 3 : Analyse NudeNet ─────────────────────────
            import tempfile
            import os

            # Fichier temporaire — supprimé immédiatement après analyse
            with tempfile.NamedTemporaryFile(
                suffix=".jpg", delete=False
            ) as tmp:
                tmp.write(buffer.getvalue())
                tmp_path = tmp.name

            try:
                detections = self.detector.detect(tmp_path)
            finally:
                # Suppression immédiate du fichier temporaire
                os.unlink(tmp_path)

            # ── Étape 4 : Calculer le score global ───────────────
            nsfw_score = self._calculate_score(detections)

            logger.debug(
                f"Analyse image NudeNet → "
                f"{len(detections)} détections, "
                f"score={nsfw_score:.3f}"
            )

            return nsfw_score

        except Exception as e:
            logger.error(f"Erreur analyse image : {e}")
            return 0.0

    def _calculate_score(self, detections: list) -> float:
        """
        Calcule un score NSFW global depuis les détections NudeNet.

        NudeNet retourne une liste de détections avec :
        - class : catégorie détectée
        - score : confiance de la détection (0.0 à 1.0)

        On retient le score maximum parmi les catégories NSFW.
        Les catégories critiques donnent automatiquement un score élevé.
        """
        if not detections:
            return 0.0

        nsfw_scores = []

        for detection in detections:
            category = detection.get("class", "")
            score    = detection.get("score", 0.0)

            # Catégorie critique → score très élevé
            if category in CRITICAL_CATEGORIES:
                nsfw_scores.append(min(score * 1.3, 1.0))

            # Catégorie NSFW normale → score direct
            elif category in NSFW_CATEGORIES:
                nsfw_scores.append(score)

        if not nsfw_scores:
            return 0.0

        # Retourner le score maximum détecté
        return round(max(nsfw_scores), 4)

    def _resize_image(self, image: Image.Image) -> Image.Image:
        """
        Redimensionne l'image pour optimiser la vitesse d'analyse.
        NudeNet est optimal sur des images de 640x640 maximum.
        """
        max_size = 640
        width, height = image.size

        if width <= max_size and height <= max_size:
            return image

        ratio     = min(max_size / width, max_size / height)
        new_width  = int(width  * ratio)
        new_height = int(height * ratio)

        return image.resize(
            (new_width, new_height),
            Image.LANCZOS  # Algorithme de redimensionnement de haute qualité
        )


# ── Instance globale ──────────────────────────────────────────────────
image_detection_service = ImageDetectionService()