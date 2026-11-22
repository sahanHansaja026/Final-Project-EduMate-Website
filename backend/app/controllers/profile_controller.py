"""HTTP handling layer for user profile management."""

from typing import Optional

from fastapi import HTTPException, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.profile import ProfileResponse, PushNotifications
from app.services import profile_service


def get_profile(email: str, current_user: User, db: Session) -> ProfileResponse:
    """Retrieve a user profile by email, enforcing ownership."""
    return profile_service.get_profile(db, email, current_user)


def get_user_name_by_email(email: str, current_user: User, db: Session) -> dict:
    """Retrieve the display names of a user by email, enforcing ownership."""
    return profile_service.get_user_name_by_email(db, email, current_user)


def get_profile_photo(email: str, current_user: User, db: Session) -> Response:
    """Serve the raw profile photo bytes, enforcing ownership."""
    photo = profile_service.get_profile_photo(db, email, current_user)

    if photo is None:
        raise HTTPException(status_code=404, detail="Profile photo not found")

    return Response(content=photo, media_type="image/jpeg")


async def create_or_update_profile(
    db: Session,
    current_user: User,
    username: str,
    about: Optional[str],
    first_name: str,
    last_name: str,
    email: str,
    country: str,
    street_address: str,
    city: str,
    region: str,
    postal_code: str,
    notify_comments: bool,
    notify_candidates: bool,
    notify_offers: bool,
    push: PushNotifications,
    photo: Optional[UploadFile],
    coverPhoto: Optional[UploadFile],
    profile_id: Optional[int] = None,
) -> ProfileResponse:
    """Create or update a user profile (HTTP layer: multipart form + file uploads)."""
    photo_bytes = await photo.read() if photo else None
    cover_bytes = await coverPhoto.read() if coverPhoto else None

    try:
        return profile_service.create_or_update_profile(
            db,
            current_user=current_user,
            username=username,
            about=about,
            first_name=first_name,
            last_name=last_name,
            email=email,
            country=country,
            street_address=street_address,
            city=city,
            region=region,
            postal_code=postal_code,
            notify_comments=notify_comments,
            notify_candidates=notify_candidates,
            notify_offers=notify_offers,
            push_notifications=push,
            photo=photo_bytes,
            cover_photo=cover_bytes,
            profile_id=profile_id,
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving profile: {e}")
