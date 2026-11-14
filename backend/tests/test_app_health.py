"""Smoke tests proving the FastAPI application boots and serves requests."""

from fastapi.testclient import TestClient

from app.main import app


def test_root_health_check(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "API running"}


def test_application_imports_without_database():
    """Importing the app must not require a live database connection."""
    assert app.title == "FastAPI"
    assert len(app.routes) > 0


def test_openapi_schema_exposes_core_endpoints(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/" in paths
    assert "/auth/signup" in paths
    assert "/auth/login" in paths
    assert "/modules/" in paths


def test_docs_are_served(client):
    assert client.get("/docs").status_code == 200


def test_unknown_route_returns_404(client):
    assert client.get("/this-route-does-not-exist").status_code == 404


def test_cors_middleware_is_configured():
    middleware_names = {middleware.cls.__name__ for middleware in app.user_middleware}

    assert "CORSMiddleware" in middleware_names
