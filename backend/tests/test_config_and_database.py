"""Tests for application settings and the database session dependency."""

import pytest

from app.core.config import settings
from app.core.database import get_db


def test_settings_expose_expected_defaults():
    assert settings.ALGORITHM == "HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES > 0
    assert settings.DATABASE_URL
    assert isinstance(settings.DEBUG, bool)


def test_secret_key_is_configured_for_tests():
    # conftest.py sets SECRET_KEY before the app is imported.
    assert settings.SECRET_KEY


def test_get_db_yields_a_session_and_closes_it():
    dependency = get_db()

    session = next(dependency)
    assert session is not None

    with pytest.raises(StopIteration):
        next(dependency)
