"""Validation tests for the request/response schemas used by the auth routes."""

import pytest
from pydantic import ValidationError

from app.schemas.auth import LoginSchema, SignupSchema, TokenSchema, UserOut


def test_signup_schema_accepts_valid_payload():
    payload = SignupSchema(email="student@example.com", password="strong-password")

    assert payload.email == "student@example.com"
    assert payload.password == "strong-password"


def test_signup_schema_rejects_invalid_email():
    with pytest.raises(ValidationError):
        SignupSchema(email="not-an-email", password="strong-password")


def test_signup_schema_requires_password():
    with pytest.raises(ValidationError):
        SignupSchema(email="student@example.com")


def test_login_schema_defaults_remember_me_to_false():
    payload = LoginSchema(email="student@example.com", password="secret")

    assert payload.remember_me is False


def test_token_schema_serializes_user():
    token = TokenSchema(
        access_token="access",
        refresh_token="refresh",
        token_type="bearer",
        user=UserOut(id=1, email="student@example.com"),
    )

    assert token.user.id == 1
    assert token.model_dump()["user"]["email"] == "student@example.com"
