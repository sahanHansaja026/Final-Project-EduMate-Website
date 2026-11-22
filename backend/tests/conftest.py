"""Shared pytest setup for the EduMate backend test suite.

Important: ``backend/app`` reads configuration and builds database engines at
import time, so the test environment has to be configured *before* any ``app.*``
module is imported. Keeping that logic here means the suite can be run with a
plain ``python -m pytest`` and never touches a developer's real database.

The suite uses its own database (``TEST_DATABASE_URL``, defaulting to an
in-memory SQLite database) and rolls every transaction back after each test, so
development and production data can never be modified by the tests.
"""

import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Make the backend package importable (``app.*`` and the legacy top-level
# modules such as ``database``) regardless of the directory pytest is run from.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

# Hermetic environment. Tests always run against the isolated test database.
os.environ.setdefault("TEST_DATABASE_URL", "sqlite://")
os.environ.setdefault("DATABASE_URL", os.environ["TEST_DATABASE_URL"])
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("DEBUG", "False")


@pytest.fixture(scope="session")
def test_engine():
    """Create the engine for the isolated test database and its tables."""
    from app.core.database import Base, create_database_engine

    test_engine = create_database_engine()
    Base.metadata.create_all(bind=test_engine)
    return test_engine


@pytest.fixture
def db_session(test_engine):
    """Provide a transactional database session that is rolled back after each test."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session):
    """FastAPI test client wired to the transactional test database session."""
    from app.core.database import get_db
    from app.main import app

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.pop(get_db, None)
