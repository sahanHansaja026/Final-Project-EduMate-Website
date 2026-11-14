"""Shared pytest setup for the EduMate backend test suite.

Important: ``backend/app`` reads configuration and builds database engines at
import time, so the test environment has to be configured *before* any ``app.*``
module is imported. Keeping that logic here means the suite can be run with a
plain ``python -m pytest`` and never touches a developer's real database.
"""

import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Make the backend package importable (``app.*`` and the legacy top-level
# modules such as ``database``) regardless of the directory pytest is run from.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

# Hermetic environment. Set TEST_DATABASE_URL to point the suite at a real
# database when running integration checks locally.
os.environ["DATABASE_URL"] = os.getenv("TEST_DATABASE_URL", "sqlite://")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ENVIRONMENT", "test")


@pytest.fixture(scope="session")
def client():
    """FastAPI test client with the application lifespan handled correctly."""
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client
