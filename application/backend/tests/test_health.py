# tests/test_health.py
# Tests automatisés pour le endpoint /health.
#
# Ces tests vérifient que le serveur répond correctement
# et que tous les champs de la réponse sont présents.

import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_health_status_ok():
    """
    Vérifie que le serveur répond avec status 'ok'
    """
    async with AsyncClient(
        transport = ASGITransport(app=app),
        base_url  = "http://test"
    ) as client:
        response = await client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"]  == "ok"


@pytest.mark.asyncio
async def test_health_contains_required_fields():
    """
    Vérifie que tous les champs requis sont présents
    """
    async with AsyncClient(
        transport = ASGITransport(app=app),
        base_url  = "http://test"
    ) as client:
        response = await client.get("/api/v1/health")

    data = response.json()
    assert "status"        in data
    assert "message"       in data
    assert "version"       in data
    assert "environment"   in data
    assert "models_loaded" in data
    assert "timestamp"     in data


@pytest.mark.asyncio
async def test_health_version_correct():
    """
    Vérifie que la version retournée est correcte
    """
    async with AsyncClient(
        transport = ASGITransport(app=app),
        base_url  = "http://test"
    ) as client:
        response = await client.get("/api/v1/health")

    data = response.json()
    assert data["version"] == "1.0.0"