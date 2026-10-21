# app/services/push_service.py
# Envoi de notifications push aux parents via Firebase Cloud Messaging (FCM).
#
# Dégradé proprement : si la librairie firebase-admin n'est pas installée ou
# si le fichier de compte de service est absent, les push sont désactivés et le
# reste de l'application continue de fonctionner (comme pour OpenAI).

import os
import threading

from loguru import logger

from app.core.config import settings

_initialized = False
_enabled = False
_lock = threading.Lock()


def _ensure_initialized() -> bool:
    """Initialise Firebase Admin une seule fois. Retourne True si le push est utilisable."""
    global _initialized, _enabled
    if _initialized:
        return _enabled

    with _lock:
        if _initialized:
            return _enabled
        _initialized = True
        try:
            import json
            import firebase_admin
            from firebase_admin import credentials

            # 1) Variable d'environnement (JSON collé) — pratique sur Railway.
            # 2) Sinon fichier local (dev).
            raw_json = settings.FIREBASE_CREDENTIALS_JSON.strip()
            if raw_json:
                cred = credentials.Certificate(json.loads(raw_json))
            elif os.path.exists(settings.FIREBASE_CREDENTIALS_FILE):
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_FILE)
            else:
                logger.warning(
                    "Push FCM désactivé — ni FIREBASE_CREDENTIALS_JSON ni "
                    f"{settings.FIREBASE_CREDENTIALS_FILE} disponibles"
                )
                _enabled = False
                return False

            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            _enabled = True
            logger.info("✅ Push FCM initialisé (Firebase Admin)")
        except ImportError:
            logger.warning("Push FCM désactivé — librairie firebase-admin non installée")
            _enabled = False
        except Exception as e:
            logger.error(f"Push FCM désactivé — erreur d'initialisation : {e}")
            _enabled = False
        return _enabled


def send_push(token: str, title: str, body: str) -> None:
    """
    Envoie une notification push à un appareil. Best-effort et non bloquant :
    toute erreur est journalisée sans interrompre l'appelant.
    """
    if not token:
        return
    if not _ensure_initialized():
        return

    def _worker():
        try:
            from firebase_admin import messaging
            message = messaging.Message(
                notification = messaging.Notification(title=title, body=body),
                token        = token,
            )
            messaging.send(message)
            logger.debug(f"Push envoyé → {title}")
        except Exception as e:
            logger.warning(f"Échec d'envoi push : {e}")

    # Envoi dans un thread : l'appel réseau FCM ne doit pas retarder la réponse
    # HTTP en cours (ex: la réponse /detect à l'app enfant).
    threading.Thread(target=_worker, daemon=True).start()
