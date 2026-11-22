"""HTTP handling layer for user management."""

from sqlalchemy.orm import Session

from app.schemas.user import LoginSchema, SignupSchema, TokenSchema
from app.services import user_service


def signup(signup_data: SignupSchema, db: Session) -> dict:
    """Register a new user (HTTP layer: request validated by the schema)."""
    return user_service.signup(signup_data, db)


def login(login_data: LoginSchema, db: Session) -> TokenSchema:
    """Authenticate a user and return tokens (HTTP layer: request validated by the schema)."""
    return user_service.login(login_data, db)


def logout(refresh_token: str, db: Session) -> dict:
    """Invalidate a refresh token (HTTP layer: token provided by the client)."""
    return user_service.logout(refresh_token, db)
