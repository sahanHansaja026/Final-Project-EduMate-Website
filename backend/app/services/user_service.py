"""Business logic layer for user management."""

import base64
from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.profile import Profile
from app.models.subscription import PlanEnum, Subscription
from app.repositories import user_repository
from app.schemas.profile import Notifications, ProfileResponse, PushNotifications
from app.schemas.user import LoginSchema, SignupSchema, TokenSchema, UserOut


def _to_profile_response(profile: Profile) -> ProfileResponse:
    """Map a ``Profile`` ORM instance to its API response without any
    sensitive or binary payload leaking into the response body."""
    photo_b64 = base64.b64encode(profile.photo).decode("utf-8") if profile.photo else None
    cover_b64 = base64.b64encode(profile.cover_photo).decode("utf-8") if profile.cover_photo else None

    return ProfileResponse(
        id=profile.id,
        username=profile.username,
        about=profile.about,
        firstName=profile.first_name,
        lastName=profile.last_name,
        email=profile.email,
        country=profile.country,
        streetAddress=profile.street_address,
        city=profile.city,
        region=profile.region,
        postalCode=profile.postal_code,
        notifications=Notifications(
            comments=profile.notify_comments,
            candidates=profile.notify_candidates,
            offers=profile.notify_offers,
            push=profile.push_notifications,
        ),
        photo=photo_b64,
        coverPhoto=cover_b64,
    )


# ---------------- USER ACCOUNT: CREATE / AUTHENTICATE ----------------
def signup(signup_data: SignupSchema, db: Session) -> dict:
    """Register a new user and provision the free subscription plan."""
    if user_repository.get_user_by_email(db, signup_data.email) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    user = user_repository.create_user(db, signup_data.email, hash_password(signup_data.password))

    db.add(
        Subscription(
            user_id=user.user_id,
            user_email=user.email,
            plan_name=PlanEnum.free,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow(),
            status="active",
        )
    )
    db.commit()

    return {"message": "User registered successfully", "user_id": user.user_id}


def login(login_data: LoginSchema, db: Session) -> TokenSchema:
    """Authenticate a user and issue access/refresh tokens."""
    user = user_repository.get_user_by_email(db, login_data.email)

    if user is None or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    refresh_days = 60 if login_data.remember_me else 30

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email}, days=refresh_days)

    user.refresh_token = refresh_token
    db.commit()

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserOut(id=user.user_id, email=user.email),
    )


def logout(refresh_token: str, db: Session) -> dict:
    """Invalidate the refresh token of a logged out session."""
    user = user_repository.get_user_by_refresh_token(db, refresh_token)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user.refresh_token = None
    db.commit()

    return {"message": "Logged out successfully"}


# ---------------- USER PROFILE: RETRIEVE / UPDATE ----------------
def get_profile(db: Session, email: str) -> ProfileResponse:
    """Retrieve a user profile by email."""
    profile = db.query(Profile).filter(Profile.email == email).first()

    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    return _to_profile_response(profile)


def get_user_name_by_email(db: Session, email: str) -> dict:
    """Retrieve the display names of a user profile by email."""
    profile = db.query(Profile).filter(Profile.email == email).first()

    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "email": profile.email,
        "firstName": profile.first_name,
        "lastName": profile.last_name,
    }


def get_profile_photo(db: Session, email: str) -> Optional[bytes]:
    """Return the raw profile photo bytes for the given email."""
    profile = db.query(Profile).filter(Profile.email == email).first()

    if profile is None or not profile.photo:
        return None

    return bytes(profile.photo)


def create_or_update_profile(
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
    push_notifications: PushNotifications,
    photo: Optional[bytes],
    cover_photo: Optional[bytes],
) -> ProfileResponse:
    """Create or update the profile of a user."""
    profile = db.query(Profile).filter(Profile.email == email).first()

    if profile is None:
        # Create new profile
        profile = Profile(
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
            push_notifications=push_notifications,
            photo=photo,
            cover_photo=cover_photo,
        )
        db.add(profile)
    else:
        # Update existing profile
        profile.username = username
        profile.about = about
        profile.first_name = first_name
        profile.last_name = last_name
        profile.country = country
        profile.street_address = street_address
        profile.city = city
        profile.region = region
        profile.postal_code = postal_code
        profile.notify_comments = notify_comments
        profile.notify_candidates = notify_candidates
        profile.notify_offers = notify_offers
        profile.push_notifications = push_notifications
        if photo:
            profile.photo = photo
        if cover_photo:
            profile.cover_photo = cover_photo

    db.commit()
    db.refresh(profile)

    return _to_profile_response(profile)
