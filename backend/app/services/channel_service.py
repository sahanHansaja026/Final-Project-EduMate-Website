"""Business logic for channel management and channel-level authorization."""

import json
from typing import List, Optional

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from app.models.channel import Channel, ChannelVisibilityEnum
from app.repositories import channel_repository
from services.s3_service import delete_file, upload_file

OWNER_ROLE = "owner"
CO_HOST_ROLE = "co_host"


# ---------------- MEMBER / CO-HOST HELPERS ----------------
def _member_email(member) -> Optional[str]:
    """Return a normalized email from a channel member entry.

    Channel members are stored as a list of email strings, but older rows may
    contain dictionaries with an ``email`` key. Both shapes are accepted so
    existing data keeps working after the refactor.
    """
    if isinstance(member, str):
        email = member.strip().lower()
        return email or None

    if isinstance(member, dict):
        email = member.get("email")
        if isinstance(email, str):
            normalized = email.strip().lower()
            return normalized or None

    return None


def normalize_member_emails(members) -> List[str]:
    """Normalize a list of channel member entries into unique email strings."""
    if not isinstance(members, list):
        raise ValueError("Channel members must be a list")

    normalized: List[str] = []
    seen = set()

    for member in members:
        email = _member_email(member)
        if email and email not in seen:
            seen.add(email)
            normalized.append(email)

    return normalized


def parse_member_emails(raw_value: str, error_detail: str) -> List[str]:
    """Parse the JSON-encoded member list submitted by the client."""
    try:
        parsed = json.loads(raw_value)
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail=error_detail)

    if not isinstance(parsed, list):
        raise HTTPException(status_code=400, detail=error_detail)

    return normalize_member_emails(parsed)


def _channel_members(channel: Channel) -> List:
    """Return the channel member list, tolerating legacy malformed values."""
    members = channel.co_hosts_and_faculty_members or []

    if isinstance(members, str):
        try:
            members = json.loads(members)
        except (TypeError, ValueError):
            return []

    return members if isinstance(members, list) else []


# ---------------- LOOKUPS ----------------
def get_channel_or_404(db: Session, channel_id: int) -> Channel:
    """Return a channel or raise a ``404`` when it does not exist."""
    channel = channel_repository.get_channel_by_id(db, channel_id)

    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")

    return channel


def resolve_actor_user_id(
    db: Session,
    user_id: Optional[int],
    email: Optional[str],
) -> Optional[int]:
    """Resolve the acting account id from an explicit id or email."""
    if user_id is not None:
        return user_id

    if email:
        user = channel_repository.get_user_by_email(db, email)
        return user.user_id if user else None

    return None


# ---------------- AUTHORIZATION ----------------
def get_channel_role(
    channel: Channel,
    user_id: Optional[int] = None,
    email: Optional[str] = None,
) -> Optional[str]:
    """Return ``owner``, ``co_host`` or ``None`` for the given actor."""
    if user_id is not None and channel.user_id == user_id:
        return OWNER_ROLE

    if email:
        normalized_email = email.strip().lower()
        for member in _channel_members(channel):
            if _member_email(member) == normalized_email:
                return CO_HOST_ROLE

    return None


def require_channel_role(
    channel: Channel,
    user_id: Optional[int] = None,
    email: Optional[str] = None,
    allow_co_host: bool = True,
) -> str:
    """Require channel access and return the actor's role."""
    role = get_channel_role(channel, user_id=user_id, email=email)

    if role is None:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this channel",
        )

    if role == CO_HOST_ROLE and not allow_co_host:
        raise HTTPException(
            status_code=403,
            detail="Only the channel owner can perform this operation",
        )

    return role


def require_channel_owner(
    db: Session,
    channel: Channel,
    user_id: Optional[int] = None,
    email: Optional[str] = None,
) -> int:
    """Require that the actor owns the channel and return the owner id."""
    actor_user_id = resolve_actor_user_id(db, user_id=user_id, email=email)

    if actor_user_id is None:
        raise HTTPException(
            status_code=403,
            detail="Channel owner verification is required",
        )

    if channel.user_id != actor_user_id:
        raise HTTPException(
            status_code=403,
            detail="Only the channel owner can perform this operation",
        )

    return actor_user_id


def authorize_channel_access(
    db: Session,
    channel_id: int,
    current_user_id: int,
    current_email: str,
) -> dict:
    """Return the owner/co-host authorization decision for a channel."""
    channel = get_channel_or_404(db, channel_id)
    role = get_channel_role(
        channel,
        user_id=current_user_id,
        email=current_email,
    )

    return {
        "authorized": role is not None,
        "role": role,
    }


# ---------------- IMAGE / ASSET HELPERS ----------------
def _upload_image(
    file: Optional[UploadFile],
    folder: str,
    error_prefix: str,
) -> Optional[str]:
    """Upload an image to S3, mapping storage failures to ``500`` errors."""
    if file is None or not getattr(file, "filename", None):
        return None

    try:
        return upload_file(file, folder=folder)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"{error_prefix}: {str(exc)}",
        )


def _delete_remote_asset(file_url: Optional[str]) -> None:
    """Delete a previously stored S3 asset when it points at the bucket."""
    if file_url and "amazonaws.com" in file_url:
        # ``delete_file`` already swallows and logs storage errors.
        delete_file(file_url)


# ---------------- CHANNEL READ OPERATIONS ----------------
def get_channels(db: Session) -> List[Channel]:
    """Return every channel."""
    return channel_repository.get_all_channels(db)


def get_channels_by_user(db: Session, user_id: int) -> List[Channel]:
    """Return the channels owned by ``user_id``."""
    return channel_repository.get_channels_by_user(db, user_id)


def get_public_channels(db: Session) -> List[Channel]:
    """Return the public channel directory."""
    return channel_repository.get_public_channels(db)


def get_channel(db: Session, channel_id: int) -> Channel:
    """Return a single channel or raise ``404``."""
    return get_channel_or_404(db, channel_id)


# ---------------- CHANNEL WRITE OPERATIONS ----------------
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
    cover_image: Optional[UploadFile] = None,
    logo_image: Optional[UploadFile] = None,
) -> Channel:
    """Create a channel owned by an existing account."""
    if channel_repository.get_user_by_id(db, user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")

    faculty_list = parse_member_emails(
        co_hosts_and_faculty_members,
        error_detail="Invalid faculty members JSON format",
    )

    cover_path = _upload_image(
        cover_image,
        folder="channels/covers",
        error_prefix="Cover image upload failed",
    )
    logo_path = _upload_image(
        logo_image,
        folder="channels/logos",
        error_prefix="Logo image upload failed",
    )

    channel = Channel(
        user_id=user_id,
        channel_name=channel_name,
        description=description,
        institute_legal_name=institute_legal_name,
        institute_owner_full_name=institute_owner_full_name,
        physical_corporate_address=physical_corporate_address,
        co_hosts_and_faculty_members=faculty_list,
        visibility=visibility,
        official_website_link=official_website_link,
        facebook_portal_link=facebook_portal_link,
        cover_image=cover_path,
        logo_image=logo_path,
    )

    return channel_repository.create_channel(db, channel)


def update_channel(
    db: Session,
    channel_id: int,
    user_id: Optional[int] = None,
    current_email: Optional[str] = None,
    channel_name: Optional[str] = None,
    description: Optional[str] = None,
    institute_legal_name: Optional[str] = None,
    institute_owner_full_name: Optional[str] = None,
    physical_corporate_address: Optional[str] = None,
    co_hosts_and_faculty_members: Optional[str] = None,
    visibility: Optional[ChannelVisibilityEnum] = None,
    official_website_link: Optional[str] = None,
    facebook_portal_link: Optional[str] = None,
    cover_image: Optional[UploadFile] = None,
    logo_image: Optional[UploadFile] = None,
) -> Channel:
    """Update a channel after verifying that the actor owns it."""
    channel = get_channel_or_404(db, channel_id)
    require_channel_owner(
        db,
        channel,
        user_id=user_id,
        email=current_email,
    )

    if channel_name is not None:
        channel.channel_name = channel_name

    if description is not None:
        channel.description = description

    if institute_legal_name is not None:
        channel.institute_legal_name = institute_legal_name

    if institute_owner_full_name is not None:
        channel.institute_owner_full_name = institute_owner_full_name

    if physical_corporate_address is not None:
        channel.physical_corporate_address = physical_corporate_address

    if visibility is not None:
        channel.visibility = visibility

    if official_website_link is not None:
        channel.official_website_link = official_website_link

    if facebook_portal_link is not None:
        channel.facebook_portal_link = facebook_portal_link

    if co_hosts_and_faculty_members is not None:
        channel.co_hosts_and_faculty_members = parse_member_emails(
            co_hosts_and_faculty_members,
            error_detail=(
                "co_hosts_and_faculty_members must be a JSON array of emails"
            ),
        )
        # SQLAlchemy does not detect in-place ARRAY/JSON mutations reliably.
        flag_modified(channel, "co_hosts_and_faculty_members")

    if cover_image is not None and getattr(cover_image, "filename", None):
        _delete_remote_asset(channel.cover_image)
        channel.cover_image = _upload_image(
            cover_image,
            folder="channels/covers",
            error_prefix="Cover upload failed",
        )

    if logo_image is not None and getattr(logo_image, "filename", None):
        _delete_remote_asset(channel.logo_image)
        channel.logo_image = _upload_image(
            logo_image,
            folder="channels/logos",
            error_prefix="Logo upload failed",
        )

    return channel_repository.update_channel(db, channel)


def delete_channel(
    db: Session,
    channel_id: int,
    user_id: Optional[int] = None,
    current_email: Optional[str] = None,
) -> dict:
    """Delete a channel and its S3 assets after verifying ownership."""
    channel = get_channel_or_404(db, channel_id)
    require_channel_owner(
        db,
        channel,
        user_id=user_id,
        email=current_email,
    )

    _delete_remote_asset(channel.cover_image)
    _delete_remote_asset(channel.logo_image)

    channel_repository.delete_channel(db, channel)

    return {"message": "Channel and its linked cloud assets deleted successfully"}
