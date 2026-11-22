"""Service and repository tests for the profile management module."""

import pytest
from fastapi import HTTPException

from app.models.profile import Profile
from app.models.user import User
from app.repositories import profile_repository
from app.schemas.profile import PushNotifications
from app.services import profile_service


def _make_user(email: str) -> User:
    """Build a minimal user instance for ownership checks."""
    return User(email=email, hashed_password="hashed-password")


def _persist_profile(db_session, email: str = "profile@example.com") -> Profile:
    """Persist a minimal profile owned by the given email."""
    profile = Profile(
        username="newuser",
        about="Hello there",
        first_name="John",
        last_name="Doe",
        email=email,
        country="United States",
        street_address="Street 1",
        city="City",
        region="Region",
        postal_code="12345",
        notify_comments=True,
        notify_candidates=False,
        notify_offers=False,
        push_notifications=PushNotifications.everything,
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)
    return profile


def test_profile_repository_returns_profile_by_email_and_id(db_session):
    """Profile lookups must resolve by email and by primary key."""
    profile = _persist_profile(db_session)

    assert profile_repository.get_profile_by_email(db_session, profile.email).id == profile.id
    assert profile_repository.get_profile_by_id(db_session, profile.id).id == profile.id
    assert profile_repository.get_profile_by_email(db_session, "missing@example.com") is None


def test_service_get_profile_returns_profile_for_owner(db_session):
    """The owner must receive their own profile payload."""
    _persist_profile(db_session)

    response = profile_service.get_profile(db_session, "profile@example.com", _make_user("profile@example.com"))

    assert response.email == "profile@example.com"
    assert response.username == "newuser"
    assert response.about == "Hello there"


def test_service_get_profile_returns_404_when_profile_missing(db_session):
    """A missing profile must surface a not found error."""
    with pytest.raises(HTTPException) as exc_info:
        profile_service.get_profile(db_session, "ghost@example.com", _make_user("ghost@example.com"))

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Profile not found"


def test_service_get_profile_rejects_other_user(db_session):
    """Cross-user profile reads must be forbidden."""
    _persist_profile(db_session)

    with pytest.raises(HTTPException) as exc_info:
        profile_service.get_profile(db_session, "profile@example.com", _make_user("student@example.com"))

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Not authorized to access this resource"


def test_service_create_or_update_profile_creates_then_updates(db_session):
    """Create a profile for the owner, then update it through its profile id."""
    user = _make_user("profile@example.com")

    created = profile_service.create_or_update_profile(
        db_session,
        current_user=user,
        username="newuser",
        about="Hello there",
        first_name="John",
        last_name="Doe",
        email="profile@example.com",
        country="United States",
        street_address="Street 1",
        city="City",
        region="Region",
        postal_code="12345",
        notify_comments=True,
        notify_candidates=False,
        notify_offers=False,
        push_notifications=PushNotifications.everything,
        photo=None,
        cover_photo=None,
    )

    assert created.email == "profile@example.com"
    assert created.username == "newuser"

    updated = profile_service.create_or_update_profile(
        db_session,
        current_user=user,
        username="updateduser",
        about="Updated about",
        first_name="Jane",
        last_name="Doe",
        email="profile@example.com",
        country="United States",
        street_address="Street 2",
        city="City",
        region="Region",
        postal_code="67890",
        notify_comments=False,
        notify_candidates=True,
        notify_offers=True,
        push_notifications=PushNotifications.none,
        photo=None,
        cover_photo=None,
        profile_id=created.id,
    )

    assert updated.username == "updateduser"
    assert updated.about == "Updated about"
    assert updated.postalCode == "67890"


def test_service_create_or_update_profile_rejects_other_user(db_session):
    """Cross-user profile updates must be forbidden."""
    user = _make_user("profile@example.com")
    created = profile_service.create_or_update_profile(
        db_session,
        current_user=user,
        username="newuser",
        about="Hello there",
        first_name="John",
        last_name="Doe",
        email="profile@example.com",
        country="United States",
        street_address="Street 1",
        city="City",
        region="Region",
        postal_code="12345",
        notify_comments=True,
        notify_candidates=False,
        notify_offers=False,
        push_notifications=PushNotifications.everything,
        photo=None,
        cover_photo=None,
    )

    attacker = _make_user("attacker@example.com")
    with pytest.raises(HTTPException) as exc_info:
        profile_service.create_or_update_profile(
            db_session,
            current_user=attacker,
            username="hijacked",
            about="Malicious update",
            first_name="Attacker",
            last_name="McAttack",
            email="profile@example.com",
            country="United States",
            street_address="Street 1",
            city="City",
            region="Region",
            postal_code="12345",
            notify_comments=False,
            notify_candidates=False,
            notify_offers=False,
            push_notifications=PushNotifications.none,
            photo=None,
            cover_photo=None,
            profile_id=created.id,
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Not authorized to update this profile"
