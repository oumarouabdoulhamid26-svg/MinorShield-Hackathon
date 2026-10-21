# app/services/ocr_service.py
# Module OCR optimisé — prétraitement minimal pour meilleure précision.

import sys
import pytesseract
from PIL import Image
import io
from loguru import logger

# Sous Windows, Tesseract n'est pas dans le PATH → on pointe l'exécutable.
# Sous Linux (Railway/Docker), il est installé via apt et déjà dans le PATH,
# donc on ne force aucun chemin.
if sys.platform == "win32":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

OCR_CONFIG = "--psm 3 --oem 3"


class OCRService:
    """
    Service d'extraction de texte depuis une image.
    Prétraitement minimal pour préserver la lisibilité du texte.
    """

    def extract_text(self, image_bytes: bytes) -> str:
        """
        Extrait le texte visible dans une image.
        """
        try:
            # ── Étape 1 : Charger l'image ─────────────────────────
            image = Image.open(io.BytesIO(image_bytes))

            # ── Étape 2 : Conversion en niveaux de gris ───────────
            # Prétraitement minimal — évite de déformer le texte
            image = image.convert("L")

            # ── Étape 3 : Extraire le texte ───────────────────────
            raw_text = pytesseract.image_to_string(
                image,
                lang    = "fra+eng",
                config  = OCR_CONFIG,
                # 8s (au lieu de 5) : l'app enfant envoie désormais une image plus
                # nette (meilleur OCR) qui demande un peu plus de temps à Tesseract.
                # Un timeout trop court renvoyait une chaîne vide (texte "perdu").
                timeout = 8
            )

            # ── Étape 4 : Nettoyer le texte ───────────────────────
            cleaned = self._clean_text(raw_text)

            if cleaned:
                logger.debug(f"OCR : {len(cleaned)} caractères extraits")
            else:
                logger.debug("OCR : aucun texte détecté")

            return cleaned

        except RuntimeError:
            logger.warning("OCR : timeout atteint")
            return ""
        except Exception as e:
            logger.error(f"Erreur OCR : {e}")
            return ""

    def _clean_text(self, text: str) -> str:
        """
        Nettoie le texte brut retourné par Tesseract.
        """
        if not text:
            return ""

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip() and len(line.strip()) > 2
        ]

        cleaned = " ".join(lines)
        cleaned = cleaned.replace("|", "").replace("_", " ")
        cleaned = " ".join(cleaned.split())

        return cleaned.strip()


# ── Instance globale ──────────────────────────────────────────────────
ocr_service = OCRService()