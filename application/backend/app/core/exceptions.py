# app/core/exceptions.py
# Définit toutes les erreurs possibles de l'application
# sous une forme structurée et professionnelle.

from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime
import uuid


class MinorShieldException(Exception):
    """
    Classe de base pour toutes les erreurs de l'application.
    Chaque erreur a un code unique, un message et un statut HTTP.
    """
    def __init__(
        self,
        error_code  : str,
        message     : str,
        status_code : int = 400
    ):
        self.error_code  = error_code
        self.message     = message
        self.status_code = status_code
        super().__init__(message)


# ── Erreurs spécifiques ───────────────────────────────────────────────

class InvalidMediaTypeException(MinorShieldException):
    def __init__(self, media_type: str):
        super().__init__(
            error_code  = "INVALID_MEDIA_TYPE",
            message     = f"Type de fichier non supporté : {media_type}. Utilisez JPEG, PNG ou WEBP.",
            status_code = 415
        )

class ImageTooLargeException(MinorShieldException):
    def __init__(self, size_mb: float):
        super().__init__(
            error_code  = "IMAGE_TOO_LARGE",
            message     = f"Image trop grande : {size_mb:.1f} Mo. Maximum autorisé : 5 Mo.",
            status_code = 413
        )

class ModelNotLoadedException(MinorShieldException):
    def __init__(self, model_name: str):
        super().__init__(
            error_code  = "MODEL_NOT_LOADED",
            message     = f"Le modèle {model_name} n'est pas chargé.",
            status_code = 503
        )

class UnauthorizedException(MinorShieldException):
    def __init__(self):
        super().__init__(
            error_code  = "UNAUTHORIZED",
            message     = "Clé API manquante ou invalide.",
            status_code = 401
        )

class ImageCorruptedException(MinorShieldException):
    def __init__(self):
        super().__init__(
            error_code  = "IMAGE_CORRUPTED",
            message     = "L'image reçue est corrompue ou illisible.",
            status_code = 422
        )


class ImageDimensionsTooLargeException(MinorShieldException):
    def __init__(self, width: int, height: int):
        super().__init__(
            error_code  = "IMAGE_DIMENSIONS_TOO_LARGE",
            message     = f"Image trop grande : {width}x{height} pixels.",
            status_code = 413
        )


# ── Gestionnaire global d'erreurs ─────────────────────────────────────

async def minorshield_exception_handler(
    request : Request,
    exc     : MinorShieldException
) -> JSONResponse:
    """
    Intercepte toutes les erreurs MinorShield et retourne
    une réponse JSON structurée et cohérente.
    
    Chaque erreur retournée à l'Android aura cette forme :
    {
        "error"      : "INVALID_MEDIA_TYPE",
        "message"    : "Type de fichier non supporté...",
        "timestamp"  : "2024-01-15T14:32:01",
        "request_id" : "uuid-unique"
    }
    """
    return JSONResponse(
        status_code = exc.status_code,
        content     = {
            "error"      : exc.error_code,
            "message"    : exc.message,
            "timestamp"  : datetime.utcnow().isoformat(),
            "request_id" : str(uuid.uuid4())
        }
    )
