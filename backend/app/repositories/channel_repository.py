"""Database access layer for channel management."""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.channel import Channel
from app.models.channel_modules import ChannelModule
from app.models.user import User


# ---------------- USERS ----------------
def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Return the account with the given primary key or ``None``."""
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Return the account registered with ``email`` or ``None``."""
    return db.query(User).filter(User.email == email).first()


# ---------------- CHANNELS ----------------
def get_channel_by_id(db: Session, channel_id: int) -> Optional[Channel]:
    """Return the channel with the given primary key or ``None``."""
    return db.query(Channel).filter(Channel.channel_id == channel_id).first()


def get_all_channels(db: Session) -> List[Channel]:
    """Return every channel in the directory."""
    return db.query(Channel).all()


def get_channels_by_user(db: Session, user_id: int) -> List[Channel]:
    """Return the channels owned by ``user_id``."""
    return db.query(Channel).filter(Channel.user_id == user_id).all()


def get_public_channels(db: Session) -> List[Channel]:
    """Return only channels that are visible to the public directory."""
    from app.models.channel import ChannelVisibilityEnum

    return db.query(Channel).filter(
        Channel.visibility == ChannelVisibilityEnum.public
    ).all()


def create_channel(db: Session, channel: Channel) -> Channel:
    """Persist a new channel."""
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return channel


def update_channel(db: Session, channel: Channel) -> Channel:
    """Persist changes applied to an existing channel."""
    db.commit()
    db.refresh(channel)
    return channel


def delete_channel(db: Session, channel: Channel) -> None:
    """Remove a channel from the database."""
    db.delete(channel)
    db.commit()


# ---------------- CHANNEL MODULES ----------------
def get_modules_by_channel(db: Session, channel_id: int) -> List[ChannelModule]:
    """Return the modules that belong to ``channel_id``."""
    return db.query(ChannelModule).filter(
        ChannelModule.channel_id == channel_id
    ).all()


def get_module_by_id(db: Session, module_id: int) -> Optional[ChannelModule]:
    """Return the channel module with the given primary key or ``None``."""
    return db.query(ChannelModule).filter(
        ChannelModule.module_id == module_id
    ).first()
