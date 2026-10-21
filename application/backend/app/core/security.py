# app/core/security.py
# Protège le serveur — seule l'application Android
# qui connaît la clé API peut appeler les endpoints.
#
# Comment ça fonctionne :
# L'application Android envoie la clé dans chaque requête
# via un header HTTP appelé "X-API-Key".
# Si la clé est absente ou incorrecte → requête rejetée (401)
# Si la clé est correcte → requête acceptée et traitée

import secrets

from fastapi import Security
from fastapi.security.api_key import APIKeyHeader
from app.core.config import settings
from app.core.exceptions import UnauthorizedException

# ── Définition du header de sécurité ─────────────────────────────────
# L'Android devra envoyer ce header dans chaque requête :
# Headers: { "X-API-Key": "CHANGE_ME" }
API_KEY_HEADER = APIKeyHeader(
    name       = "X-API-Key",
    auto_error = False  # On gère l'erreur manuellement ci-dessous
)


_MAX_KEY_LENGTH = 256


async def verify_api_key(
    api_key: str = Security(API_KEY_HEADER)
) -> str:
    """
    Vérifie que la clé API envoyée par l'Android est correcte.

    - Clé absente, trop longue ou incorrecte → 401
    - compare_digest() protège contre les timing attacks
    """
    if not settings.API_KEY:
        raise UnauthorizedException()

    if api_key is None:
        raise UnauthorizedException()

    # Bloquer les clés anormalement longues (DoS / timing abuse)
    if len(api_key) > _MAX_KEY_LENGTH:
        raise UnauthorizedException()

    if not secrets.compare_digest(api_key.strip(), settings.API_KEY):
        raise UnauthorizedException()

    return api_key
