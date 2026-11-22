"""Business logic layer for user profile management."""

import base64
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.profile import Profile
from app.models.user import User
from app.repositories import profile_repository
from app.schemas.profile import Notifications, ProfileResponse, PushNotifications


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


def _apply_profile_updates(
    profile: Profile,
    username: str,
    about: Optional[str],
    first_name: str,
    last_name: str,
    country: str,
    street_address: str,
    city: str,
    region: str,
    postal_code: str,
    notify_comments: bool,
    notify_candidates: bool,
    notify_offers: bool,
    push_notifications: PushNotifications,
) -> None:
    """Apply profile field updates onto an existing ``Profile`` instance."""
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


# ---------------- USER PROFILE: RETRIEVE / UPDATE ----------------
def get_profile(db: Session, email: str, current_user: User) -> ProfileResponse:
    """Retrieve a user profile by email, enforcing ownership."""
    if current_user.email != email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")

    profile = profile_repository.get_profile_by_email(db, email)

    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    return _to_profile_response(profile)


def get_user_name_by_email(db: Session, email: str, current_user: User) -> dict:
    """Retrieve the display names of a user by email, enforcing ownership."""
    if current_user.email != email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")

    profile = profile_repository.get_profile_by_email(db, email)

    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "email": profile.email,
        "firstName": profile.first_name,
        "lastName": profile.last_name,
    }


def get_profile_photo(db: Session, email: str, current_user: User) -> Optional[bytes]:
    """Return the raw profile photo bytes for the given email, enforcing ownership."""
    if current_user.email != email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")

    profile = profile_repository.get_profile_by_email(db, email)

    if profile is None or not profile.photo:
        return None

    return bytes(profile.photo)


def create_or_update_profile(
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
    push_notifications: PushNotifications,
    photo: Optional[bytes],
    cover_photo: Optional[bytes],
    profile_id: Optional[int] = None,
) -> ProfileResponse:
    """Create or update the profile of a user (optionally targeting a profile id)."""
    if profile_id is not None:
        # Update an existing profile by primary key, enforcing ownership.
        profile = profile_repository.get_profile_by_id(db, profile_id)

        if profile is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

        if profile.email != current_user.email:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this profile")

        _apply_profile_updates(
            profile,
            username=username,
            about=about,
            first_name=first_name,
            last_name=last_name,
            country=country,
            street_address=street_address,
            city=city,
            region=region,
            postal_code=postal_code,
            notify_comments=notify_comments,
            notify_candidates=notify_candidates,
            notify_offers=notify_offers,
            push_notifications=push_notifications,
        )
        if photo:
            profile.photo = photo
        if cover_photo:
            profile.cover_photo = cover_photo

        profile = profile_repository.update_profile(db, profile)
    else:
        # Enforce that a user only manages their own profile.
        if current_user.email != email:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this profile")

        profile = profile_repository.get_profile_by_email(db, email)

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
            profile = profile_repository.create_profile(db, profile)
        else:
            # Update existing profile
            _apply_profile_updates(
                profile,
                username=username,
                about=about,
                first_name=first_name,
                last_name=last_name,
                country=country,
                street_address=street_address,
                city=city,
                region=region,
                postal_code=postal_code,
                notify_comments=notify_comments,
                notify_candidates=notify_candidates,
                notify_offers=notify_offers,
                push_notifications=push_notifications,
            )
            if photo:
                profile.photo = photo
            if cover_photo:
                profile.cover_photo = cover_photo

            profile = profile_repository.update_profile(db, profile)

    return _to_profile_response(profile)
