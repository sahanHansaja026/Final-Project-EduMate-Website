"""HTTP handling layer for user management."""

from typing import Optional

from fastapi import HTTPException, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.schemas.profile import ProfileResponse, PushNotifications
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


def get_profile(email: str, db: Session) -> ProfileResponse:
    """Retrieve a user profile by email."""
    return user_service.get_profile(db, email)


def get_user_name_by_email(email: str, db: Session) -> dict:
    """Retrieve the display names of a user by email."""
    return user_service.get_user_name_by_email(db, email)


def get_profile_photo(email: str, db: Session) -> Response:
    """Serve the raw profile photo bytes."""
    photo = user_service.get_profile_photo(db, email)

    if photo is None:
        raise HTTPException(status_code=404, detail="Profile photo not found")

    return Response(content=photo, media_type="image/jpeg")


async def create_or_update_profile(
    db: Session,
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
) -> ProfileResponse:
    """Create or update a user profile (HTTP layer: multipart form + file uploads)."""
    photo_bytes = await photo.read() if photo else None
    cover_bytes = await coverPhoto.read() if coverPhoto else None

    try:
        return user_service.create_or_update_profile(
            db,
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
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving profile: {e}")
