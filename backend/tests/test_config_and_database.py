"""Tests for application settings and the database session dependency."""

import pytest

from app.core.config import settings
from app.core.database import engine, get_db


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


def test_get_db_rolls_back_and_closes_the_session_when_the_request_fails():
    dependency = get_db()
    session = next(dependency)

    with pytest.raises(RuntimeError, match="database exploded"):
        dependency.throw(RuntimeError("database exploded"))

    # The session must not be left inside a transaction after the failure.
    assert not session.in_transaction()


def test_engine_is_created_from_the_centralized_database_configuration():
    # The single shared engine must point at the active (test) database URL.
    assert engine.url.render_as_string(hide_password=True) == settings.TEST_DATABASE_URL
    assert engine.url.drivername.startswith("sqlite")


def test_database_url_respects_the_current_environment():
    assert settings.ENVIRONMENT == "test"
    assert settings.database_url == settings.TEST_DATABASE_URL
