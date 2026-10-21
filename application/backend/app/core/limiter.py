# app/core/limiter.py
# Instance partagée du rate limiter SlowAPI.
# Importée dans main.py (middleware) ET dans les endpoints (décorateur).
# Un seul limiter → compteurs cohérents.

import hashlib
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request


def _rate_limit_key(request: Request) -> str:
    """
    Clé de rate limiting : hash de la clé API si présente, sinon IP.
    Le hash évite de stocker la clé en clair dans les compteurs.
    """
    api_key = request.headers.get("X-API-Key", "").strip()
    if api_key:
        digest = hashlib.sha256(api_key.encode()).hexdigest()[:16]
        return f"key:{digest}"
    return f"ip:{get_remote_address(request)}"


limiter = Limiter(key_func=_rate_limit_key)
