"""Database access layer for user profile management."""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.profile import Profile


def get_profile_by_email(db: Session, email: str) -> Optional[Profile]:
    """Return the profile registered with ``email`` or ``None``."""
    return db.query(Profile).filter(Profile.email == email).first()


def get_profile_by_id(db: Session, profile_id: int) -> Optional[Profile]:
    """Return the profile with the given primary key or ``None``."""
    return db.query(Profile).filter(Profile.id == profile_id).first()


def create_profile(db: Session, profile: Profile) -> Profile:
    """Persist a new profile."""
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def update_profile(db: Session, profile: Profile) -> Profile:
    """Persist changes applied to an existing profile."""
    db.commit()
    db.refresh(profile)
    return profile
