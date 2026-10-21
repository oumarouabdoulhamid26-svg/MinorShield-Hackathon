# app/services/text_service.py
# Module de détection de contenu textuel inapproprié.
#
# Combine deux APIs pour une précision maximale :
# 1. OpenAI Moderation API (gratuit) — précis en anglais
# 2. HuggingFace Inference API (gratuit) — multilingue natif
#    Modèle : unitary/toxic-bert
#    Fonctionne bien en français et anglais

import os
import re
import unicodedata

from openai import OpenAI
import httpx
from loguru import logger
from app.core.config import settings


def _strip_accents(s: str) -> str:
    """Retire les accents (comparaison insensible aux accents)."""
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


def _load_local_lexicon() -> "re.Pattern | None":
    """
    Charge le lexique local (app/data/lexique_cmr.txt) et compile un motif
    qui matche n'importe quel terme, en MOT ENTIER, insensible casse/accents.
    """
    path = os.path.join(os.path.dirname(__file__), "..", "data", "lexique_cmr.txt")
    try:
        terms = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                terms.append(re.escape(_strip_accents(line.lower())))
        if not terms:
            return None
        pattern = re.compile(r"\b(?:" + "|".join(terms) + r")\b")
        logger.info(f"✅ Lexique local chargé : {len(terms)} termes")
        return pattern
    except Exception as e:
        logger.warning(f"Lexique local non chargé : {e}")
        return None


class TextDetectionService:
    """
    Service de détection de contenu textuel inapproprié.

    Combine OpenAI Moderation et HuggingFace pour couvrir :
    - Le français natif (HuggingFace)
    - L'anglais (OpenAI + HuggingFace)
    - Le contenu sexuel explicite
    - La violence et les menaces
    - Les insultes et la discrimination
    - Le harcèlement
    """

    # URL corrigée du modèle HuggingFace
    HF_MODEL_URL = (
        "https://router.huggingface.co/hf-inference/models/"
        "unitary/toxic-bert"
    )

    def __init__(self):
        """
        Initialise les deux clients au démarrage.
        """
        # ── OpenAI Moderation ─────────────────────────────────────
        if settings.EXTERNAL_TEXT_ANALYSIS_ENABLED and settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            logger.info("OpenAI Moderation initialise")
        else:
            self.client = None
            logger.warning("OpenAI Moderation desactive ou non configure")

        # ── HuggingFace ───────────────────────────────────────────
        if settings.EXTERNAL_TEXT_ANALYSIS_ENABLED and settings.HUGGINGFACE_TOKEN:
            self.hf_headers = {
                "Authorization": f"Bearer {settings.HUGGINGFACE_TOKEN}"
            }
            logger.info("✅ HuggingFace Inference API configurée")
        else:
            self.hf_headers = None
            logger.warning("HuggingFace desactive ou non configure")

        # ── Detoxify désactivé ────────────────────────────────────
        self.detoxify = None

        # ── Lexique local (français/anglais/slang CMR) ────────────
        self._lexicon = _load_local_lexicon()
        logger.info("Mode analyse texte configure")

    def analyze(self, text: str, extra_keywords: list = None) -> float:
        """
        Analyse un texte et retourne un score de dangerosité.

        Args:
            text: Texte extrait par OCR

        Returns:
            float: Score entre 0.0 et 1.0
        """
        if not text or len(text.strip()) < 3:
            return 0.0

        # ── Lexique local + mots perso de l'enfant (instantané, sans IA) ──
        # Le lexique attrape le vocabulaire local (fr camerounais, camfranglais,
        # pidgin) ; extra_keywords = mots ajoutés par le parent pour CET enfant.
        local_score = max(
            self._lexicon_score(text),
            self._extra_keywords_score(text, extra_keywords),
        )

        if not settings.EXTERNAL_TEXT_ANALYSIS_ENABLED:
            return local_score

        # ── OpenAI en priorité (rapide et fiable) ─────────────────
        # HuggingFace n'est appelé QU'EN SECOURS quand OpenAI est
        # indisponible : appeler les deux à chaque capture doublait la
        # latence (l'API HF gratuite a des démarrages à froid de plusieurs
        # secondes), ce qui rendait la détection très lente.
        if self.client is not None and settings.OPENAI_ENABLED:
            ai_score = self._analyze_openai(text)
        else:
            ai_score = self._analyze_huggingface(text)

        # Score final = le plus élevé entre l'IA et la détection locale.
        final = round(max(ai_score, local_score), 4)
        logger.debug(f"Texte → ia={ai_score:.3f}, local={local_score:.3f}, final={final:.3f}")
        return final

    def _lexicon_score(self, text: str) -> float:
        """0.95 si un terme du lexique local est présent, sinon 0.0."""
        if self._lexicon is None:
            return 0.0
        return 0.95 if self._lexicon.search(_strip_accents(text.lower())) else 0.0

    def _extra_keywords_score(self, text: str, extra_keywords: list) -> float:
        """0.95 si un mot sensible personnalisé (propre à l'enfant) est présent."""
        if not extra_keywords:
            return 0.0
        normalized = _strip_accents(text.lower())
        for kw in extra_keywords:
            k = _strip_accents(str(kw).lower()).strip()
            if k and re.search(r"\b" + re.escape(k) + r"\b", normalized):
                return 0.95
        return 0.0

    def _analyze_openai(self, text: str) -> float:
        """
        Analyse via OpenAI Moderation API.
        Très précis en anglais.
        """
        if self.client is None or not settings.OPENAI_ENABLED:
            return 0.0

        try:
            response = self.client.moderations.create(input=text)
            scores   = response.results[0].category_scores

            return max(
                scores.sexual,
                scores.sexual_minors,
                scores.violence,
                scores.harassment,
                scores.hate,
            )
        except Exception as e:
            logger.error(f"Erreur OpenAI : {e}")
            return 0.0

    def _analyze_huggingface(self, text: str) -> float:
        """
        Analyse via HuggingFace Inference API.
        Envoie le texte complet ET les mots-clés séparément.
        """
        if not self.hf_headers:
            return 0.0

        try:
            # ── Analyse du texte complet ──────────────────────────
            score_full = self._hf_request(text)

            # ── Analyse des mots importants ───────────────────────
            words = " ".join([
                w for w in text.split()
                if len(w) > 4
            ])
            score_words = self._hf_request(words) if words else 0.0

            # Prendre le maximum des deux
            final = max(score_full, score_words)

            logger.debug(
                f"HuggingFace → full={score_full:.3f}, "
                f"words={score_words:.3f}, "
                f"final={final:.3f}"
            )

            return round(final, 4)

        except Exception as e:
            logger.error(f"Erreur HuggingFace : {e}")
            return 0.0

    def _hf_request(self, text: str) -> float:
        """
        Envoie une requête à HuggingFace et retourne le score toxic.
        """
        try:
            response = httpx.post(
                self.HF_MODEL_URL,
                headers = self.hf_headers,
                json    = {"inputs": text},
                timeout = 10.0
            )

            if response.status_code != 200:
                logger.warning(f"HuggingFace status: {response.status_code}")
                return 0.0

            result = response.json()

            if isinstance(result, list) and len(result) > 0:
                scores = result[0]
                for item in scores:
                    if isinstance(item, dict):
                        label = item.get("label", "").lower()
                        score = item.get("score", 0.0)
                        if label == "toxic":
                            return round(score, 4)

            return 0.0

        except Exception as e:
            logger.error(f"Erreur HuggingFace request : {e}")
            return 0.0

    def _analyze_detoxify(self, text: str) -> float:
        """Désactivé — remplacé par HuggingFace API"""
        return 0.0


# ── Instance globale ──────────────────────────────────────────────────
text_detection_service = TextDetectionService()
