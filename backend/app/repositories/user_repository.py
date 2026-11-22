"""Database access layer for user management."""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Return the user registered with ``email`` or ``None``."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Return the user with the given primary key or ``None``."""
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_refresh_token(db: Session, refresh_token: str) -> Optional[User]:
    """Return the user that owns ``refresh_token`` or ``None``."""
    return db.query(User).filter(User.refresh_token == refresh_token).first()


def create_user(db: Session, email: str, hashed_password: str) -> User:
    """Persist a new user with a bcrypt hashed password."""
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def clear_refresh_token(db: Session, user: User) -> None:
    """Invalidate the refresh token of an authenticated user."""
    user.refresh_token = None
    db.commit()
