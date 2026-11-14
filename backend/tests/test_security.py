"""Tests for password hashing and JWT helpers in app.core.security."""

from datetime import datetime, timezone

import pytest
from jose import jwt

from app.core import security


def test_password_is_hashed_and_verifiable():
    password = "S3cure-Passw0rd!"
    hashed = security.hash_password(password)

    assert hashed != password
    assert security.verify_password(password, hashed) is True


def test_wrong_password_is_rejected():
    hashed = security.hash_password("correct-password")

    assert security.verify_password("wrong-password", hashed) is False


def test_access_token_round_trip():
    token = security.create_access_token({"sub": "student@example.com"}, days=1)

    payload = jwt.decode(
        token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
    )

    assert payload["sub"] == "student@example.com"
    assert "exp" in payload
    assert datetime.fromtimestamp(payload["exp"], tz=timezone.utc) > datetime.now(
        timezone.utc
    )


def test_refresh_token_outlives_access_token():
    access_token = security.create_access_token({"sub": "student@example.com"}, days=1)
    refresh_token = security.create_refresh_token(
        {"sub": "student@example.com"}, days=60
    )

    access_exp = jwt.decode(
        access_token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
    )["exp"]
    refresh_exp = jwt.decode(
        refresh_token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
    )["exp"]

    assert refresh_exp > access_exp


def test_token_signed_with_another_key_is_rejected():
    token = jwt.encode(
        {"sub": "attacker@example.com"},
        "a-different-key",
        algorithm=security.ALGORITHM,
    )

    with pytest.raises(Exception):
        jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])


def test_decode_access_token_returns_payload():
    token = security.create_access_token({"sub": "student@example.com"}, days=1)

    assert security.decode_access_token(token)["sub"] == "student@example.com"


def test_decode_access_token_returns_none_for_invalid_token():
    assert security.decode_access_token("not-a-jwt") is None
