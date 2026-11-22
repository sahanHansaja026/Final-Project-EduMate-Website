"""Channel management endpoints.

The route handlers in this module only deal with HTTP concerns (multipart
forms, file uploads and dependencies). Business rules and ownership checks live
in ``app.controllers.channel_controller`` and ``app.services.channel_service``.
"""

from typing import List

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from sqlalchemy.orm import Session

from app.controllers import channel_controller
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.channel import ChannelVisibilityEnum
from app.models.user import User
from app.schemas.channel import ChannelResponse

router = APIRouter(prefix="/channels", tags=["Channels"])


# -------------------------
# CREATE CHANNEL
# -------------------------
@router.post("/", response_model=ChannelResponse)
async def create_channel(
    user_id: int = Form(...),
    channel_name: str = Form(...),
    description: str = Form(None),

    institute_legal_name: str = Form(...),
    institute_owner_full_name: str = Form(...),
    physical_corporate_address: str = Form(None),

    co_hosts_and_faculty_members: str = Form("[]"),

    visibility: ChannelVisibilityEnum = Form(...),

    official_website_link: str = Form(None),
    facebook_portal_link: str = Form(None),

    cover_image: UploadFile = File(None),
    logo_image: UploadFile = File(None),

    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a channel owned by the supplied account."""
    return channel_controller.create_channel(
        db,
        user_id=user_id,
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
        current_user=current_user,
    )


# -------------------------
# GET ALL CHANNELS
# -------------------------
@router.get("/", response_model=List[ChannelResponse])
def get_all_channels(db: Session = Depends(get_db)):
    """Return every channel in the directory."""
    return channel_controller.get_channels(db)


# -------------------------
# GET BY USER
# -------------------------
@router.get("/user/{user_id}", response_model=List[ChannelResponse])
def get_channels_by_user(user_id: int, db: Session = Depends(get_db)):
    """Return the channels owned by a user."""
    return channel_controller.get_channels_by_user(db, user_id)


# -------------------------
# GET PUBLIC
# -------------------------
@router.get("/public", response_model=List[ChannelResponse])
def get_public_channels(db: Session = Depends(get_db)):
    """Return only public channels."""
    return channel_controller.get_public_channels(db)


# -------------------------
# GET BY ID
# -------------------------
@router.get("/{channel_id}", response_model=ChannelResponse)
def get_channel(channel_id: int, db: Session = Depends(get_db)):
    """Return a single channel."""
    return channel_controller.get_channel(db, channel_id)


# -------------------------
# UPDATE CHANNEL
# -------------------------
@router.put("/{channel_id}", response_model=ChannelResponse)
async def update_channel(
    channel_id: int,
    user_id: int = Form(...),
    current_email: str = Form(None),
    channel_name: str = Form(None),
    description: str = Form(None),
    institute_legal_name: str = Form(None),
    institute_owner_full_name: str = Form(None),
    physical_corporate_address: str = Form(None),
    co_hosts_and_faculty_members: str = Form(None),
    # Kept as a string because FastAPI's Pydantic-v1 compatibility layer
    # cannot build an OpenAPI schema for an optional Enum form field.
    visibility: str = Form(None),
    official_website_link: str = Form(None),
    facebook_portal_link: str = Form(None),
    cover_image: UploadFile = File(None),
    logo_image: UploadFile = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a channel after verifying ownership."""
    return channel_controller.update_channel(
        db,
        channel_id=channel_id,
        user_id=user_id,
        current_email=current_email,
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
        current_user=current_user,
    )


# -------------------------
# AUTHORIZATION CHECK
# -------------------------
@router.get("/{channel_id}/authorize")
def authorize_channel_access(
    channel_id: int,
    current_user_id: int,
    current_email: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return whether the caller is the channel owner or a co-host."""
    return channel_controller.authorize_channel_access(
        db,
        channel_id=channel_id,
        current_user_id=current_user_id,
        current_email=current_email,
        current_user=current_user,
    )


# -------------------------
# DELETE CHANNEL
# -------------------------
@router.delete("/{channel_id}")
def delete_channel(
    channel_id: int,
    user_id: int = Query(None),
    current_email: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a channel and its cloud assets after verifying ownership."""
    return channel_controller.delete_channel(
        db,
        channel_id=channel_id,
        user_id=user_id,
        current_email=current_email,
        current_user=current_user,
    )
