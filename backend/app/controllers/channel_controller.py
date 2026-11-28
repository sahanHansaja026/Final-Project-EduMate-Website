"""HTTP handling layer for channel management."""

from typing import Optional

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.channel import ChannelVisibilityEnum
from app.models.user import User
from app.services import channel_service


def _resolve_actor(
    current_user: User,
    user_id: Optional[int] = None,
    current_email: Optional[str] = None,
) -> tuple[int, str]:
    """Resolve the acting identity from the authenticated user.

    Legacy ``user_id`` / ``current_email`` parameters remain accepted for
    request compatibility, but they are only allowed to confirm the identity
    carried by the bearer token. They can never select a different actor.
    """
    if user_id is not None and current_user.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to act on behalf of another user",
        )

    if (
        current_email is not None
        and current_email.strip().lower() != current_user.email.strip().lower()
    ):
        raise HTTPException(
            status_code=403,
            detail="Authenticated user does not match current_email",
        )

    return current_user.user_id, current_user.email


# ---------------- READ OPERATIONS ----------------
def get_channels(db: Session):
    """Return every channel."""
    return channel_service.get_channels(db)


def get_channels_by_user(db: Session, user_id: int):
    """Return the channels owned by a user."""
    return channel_service.get_channels_by_user(db, user_id)


def get_public_channels(db: Session):
    """Return the public channel directory."""
    return channel_service.get_public_channels(db)


def get_channel(db: Session, channel_id: int):
    """Return a single channel."""
    return channel_service.get_channel(db, channel_id)


# ---------------- WRITE OPERATIONS ----------------
def create_channel(
    db: Session,
    user_id: int,
    channel_name: str,
    description: Optional[str],
    institute_legal_name: str,
    institute_owner_full_name: str,
    physical_corporate_address: Optional[str],
    co_hosts_and_faculty_members: str,
    visibility: ChannelVisibilityEnum,
    official_website_link: Optional[str],
    facebook_portal_link: Optional[str],
    current_user: User,
    cover_image: Optional[UploadFile] = None,
    logo_image: Optional[UploadFile] = None,
):
    """Create a channel (HTTP layer: multipart form + optional uploads)."""
    actor_user_id, _ = _resolve_actor(current_user, user_id=user_id)

    return channel_service.create_channel(
        db,
        user_id=actor_user_id,
        channel_name=channel_name,
        description=description,
        institute_legal_name=institute_legal_name,
        institute_owner_full_name=institute_owner_full_name,
        physical_corporate_address=physical_corporate_address,
        co_hosts_and_faculty_members=co_hosts_and_faculty_members,
        visibility=visibility,
        official_website_link=official_website_link,
        facebook_portal_link=facebook_portal_link,
        cover_image=cover_image,
        logo_image=logo_image,
    )


def update_channel(
    db: Session,
    channel_id: int,
    current_user: User,
    user_id: Optional[int] = None,
    current_email: Optional[str] = None,
    channel_name: Optional[str] = None,
    description: Optional[str] = None,
    institute_legal_name: Optional[str] = None,
    institute_owner_full_name: Optional[str] = None,
    physical_corporate_address: Optional[str] = None,
    co_hosts_and_faculty_members: Optional[str] = None,
    visibility: Optional[str] = None,
    official_website_link: Optional[str] = None,
    facebook_portal_link: Optional[str] = None,
    cover_image: Optional[UploadFile] = None,
    logo_image: Optional[UploadFile] = None,
):
    """Update a channel (HTTP layer: multipart form + optional uploads)."""
    actor_user_id, actor_email = _resolve_actor(
        current_user,
        user_id=user_id,
        current_email=current_email,
    )

    visibility_value = None
    if visibility is not None:
        try:
            visibility_value = ChannelVisibilityEnum(visibility)
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail="visibility must be either 'public' or 'private'",
            )

    return channel_service.update_channel(
        db,
        channel_id=channel_id,
        user_id=actor_user_id,
        current_email=actor_email,
        channel_name=channel_name,
        description=description,
        institute_legal_name=institute_legal_name,
        institute_owner_full_name=institute_owner_full_name,
        physical_corporate_address=physical_corporate_address,
        co_hosts_and_faculty_members=co_hosts_and_faculty_members,
        visibility=visibility_value,
        official_website_link=official_website_link,
        facebook_portal_link=facebook_portal_link,
        cover_image=cover_image,
        logo_image=logo_image,
    )


def delete_channel(
    db: Session,
    channel_id: int,
    current_user: User,
    user_id: Optional[int] = None,
    current_email: Optional[str] = None,
) -> dict:
    """Delete a channel after validating the authenticated actor."""
    actor_user_id, actor_email = _resolve_actor(
        current_user,
        user_id=user_id,
        current_email=current_email,
    )

    return channel_service.delete_channel(
        db,
        channel_id=channel_id,
        user_id=actor_user_id,
        current_email=actor_email,
    )


def authorize_channel_access(
    db: Session,
    channel_id: int,
    current_user_id: int,
    current_email: str,
    current_user: User,
) -> dict:
    """Return the owner/co-host authorization decision for a channel."""
    actor_user_id, actor_email = _resolve_actor(
        current_user,
        user_id=current_user_id,
        current_email=current_email,
    )

    return channel_service.authorize_channel_access(
        db,
        channel_id=channel_id,
        current_user_id=actor_user_id,
        current_email=actor_email,
    )
