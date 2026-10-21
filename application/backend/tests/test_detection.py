# tests/test_detection.py
# Tests automatisés pour le endpoint /detect.
#
# Ces tests vérifient :
# - L'authentification par clé API
# - La validation des fichiers
# - La structure de la réponse
# - Les cas limites

import pytest
from httpx import AsyncClient, ASGITransport
from main import app

# ── Clé API valide pour les tests ─────────────────────────────────────
VALID_API_KEY   = "CHANGE_ME"
INVALID_API_KEY = "mauvaise-cle"

# ── Image de test minimale (1x1 pixel JPEG) ───────────────────────────
# On crée une image minuscule en mémoire pour les tests
# sans avoir besoin d'un vrai fichier sur le disque
def create_test_image() -> bytes:
    from PIL import Image
    import io
    img    = Image.new("RGB", (100, 100), color=(255, 255, 255))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return buffer.getvalue()


def create_large_dimension_image() -> bytes:
    from PIL import Image
    import io
    img    = Image.new("RGB", (4097, 1), color=(255, 255, 255))
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


# ── Tests d'authentification ──────────────────────────────────────────

@pytest.mark.asyncio
async def test_detect_without_api_key_returns_401():
    """
    Vérifie qu'une requête sans clé API est rejetée
    """
    async with AsyncClient(
        transport = ASGITransport(app=app),
        base_url  = "http://test"
    ) as client:
        response = await client.post(
            "/api/v1/detect",
            files = {"image": ("test.jpg", create_test_image(), "image/jpeg")}
        )

    assert response.status_code == 401
    assert response.json()["error"] == "UNAUTHORIZED"


@pytest.mark.asyncio
async def test_detect_with_invalid_api_key_returns_401():
    """
    Vérifie qu'une clé API incorrecte est rejetée
    """
    async with AsyncClient(
        transport = ASGITransport(app=app),
        base_url  = "http://test"
    ) as client:
        response = await client.post(
            "/api/v1/detect",
            headers = {"X-API-Key": INVALID_API_KEY},
            files   = {"image": ("test.jpg", create_test_image(), "image/jpeg")}
        )

    assert response.status_code == 401
    assert response.json()["error"] == "UNAUTHORIZED"


# ── Tests de validation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_detect_with_invalid_file_type_returns_415():
    """
    Vérifie qu'un fichier non image est rejeté
    """
    async with AsyncClient(
        transport = ASGITransport(app=app),
        base_url  = "http://test"
    ) as client:
        response = await client.post(
            "/api/v1/detect",
            headers = {"X-API-Key": VALID_API_KEY},
            files   = {"image": ("test.txt", b"contenu texte", "text/plain")}
        )

    assert response.status_code == 415
    assert response.json()["error"] == "INVALID_MEDIA_TYPE"


@pytest.mark.asyncio
async def test_detect_with_fake_image_returns_422():
    """
    Vérifie qu'un fichier annonce comme image mais invalide est rejeté
    """
    async with AsyncClient(
        transport = ASGITransport(app=app),
        base_url  = "http://test"
    ) as client:
        response = await client.post(
            "/api/v1/detect",
            headers = {"X-API-Key": VALID_API_KEY},
            files   = {"image": ("test.jpg", b"not an image", "image/jpeg")}
        )

    assert response.status_code == 422
    assert response.json()["error"] == "IMAGE_CORRUPTED"


@pytest.mark.asyncio
async def test_detect_with_large_dimensions_returns_413():
    """
    Vérifie qu'une image trop large est rejetée avant l'analyse IA
    """
    async with AsyncClient(
        transport = ASGITransport(app=app),
        base_url  = "http://test"
    ) as client:
        response = await client.post(
            "/api/v1/detect",
            headers = {"X-API-Key": VALID_API_KEY},
            files   = {"image": ("test.png", create_large_dimension_image(), "image/png")}
        )

    assert response.status_code == 413
    assert response.json()["error"] == "IMAGE_DIMENSIONS_TOO_LARGE"


@pytest.mark.asyncio
async def test_detect_with_valid_image_returns_200():
    """
    Vérifie qu'une image valide est acceptée et analysée
    """
    async with AsyncClient(
        transport = ASGITransport(app=app),
        base_url  = "http://test"
    ) as client:
        response = await client.post(
            "/api/v1/detect",
            headers = {"X-API-Key": VALID_API_KEY},
            files   = {"image": ("test.jpg", create_test_image(), "image/jpeg")}
        )

    assert response.status_code == 200


# ── Tests de structure de réponse ─────────────────────────────────────

@pytest.mark.asyncio
async def test_detect_response_contains_required_fields():
    """
    Vérifie que tous les champs requis sont présents dans la réponse
    """
    async with AsyncClient(
        transport = ASGITransport(app=app),
        base_url  = "http://test"
    ) as client:
        response = await client.post(
            "/api/v1/detect",
            headers = {"X-API-Key": VALID_API_KEY},
            files   = {"image": ("test.jpg", create_test_image(), "image/jpeg")}
        )

    data = response.json()
    assert "request_id"     in data
    assert "nsfw_score"     in data
    assert "label"          in data
    assert "image_score"    in data
    assert "text_score"     in data
    assert "processing_ms"  in data
    assert "timestamp"      in data


@pytest.mark.asyncio
async def test_detect_scores_between_0_and_1():
    """
    Vérifie que tous les scores sont entre 0.0 et 1.0
    """
    async with AsyncClient(
        transport = ASGITransport(app=app),
        base_url  = "http://test"
    ) as client:
        response = await client.post(
            "/api/v1/detect",
            headers = {"X-API-Key": VALID_API_KEY},
            files   = {"image": ("test.jpg", create_test_image(), "image/jpeg")}
        )

    data = response.json()
    assert 0.0 <= data["nsfw_score"]  <= 1.0
    assert 0.0 <= data["image_score"] <= 1.0
    assert 0.0 <= data["text_score"]  <= 1.0


@pytest.mark.asyncio
async def test_detect_label_is_safe_or_nsfw():
    """
    Vérifie que le label est soit 'safe' soit 'nsfw'
    """
    async with AsyncClient(
        transport = ASGITransport(app=app),
        base_url  = "http://test"
    ) as client:
        response = await client.post(
            "/api/v1/detect",
            headers = {"X-API-Key": VALID_API_KEY},
            files   = {"image": ("test.jpg", create_test_image(), "image/jpeg")}
        )

    data = response.json()
    assert data["label"] in ["safe", "nsfw"]


@pytest.mark.asyncio
async def test_detect_white_image_is_safe():
    """
    Vérifie qu'une image blanche (safe) retourne label 'safe'
    """
    async with AsyncClient(
        transport = ASGITransport(app=app),
        base_url  = "http://test"
    ) as client:
        response = await client.post(
            "/api/v1/detect",
            headers = {"X-API-Key": VALID_API_KEY},
            files   = {"image": ("test.jpg", create_test_image(), "image/jpeg")}
        )

    data = response.json()
    assert data["label"]      == "safe"
    assert data["nsfw_score"] <  0.60
