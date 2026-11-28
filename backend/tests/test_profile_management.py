"""Service, repository and API tests for the profile management module."""

import pytest
from fastapi import HTTPException, status

from app.models.profile import Profile
from app.models.user import User
from app.repositories import profile_repository
from app.schemas.profile import PushNotifications
from app.services import profile_service


def _make_user(email: str) -> User:
    """Build a minimal user instance for ownership checks."""
    return User(email=email, hashed_password="hashed-password")


def _register_and_authenticate(client, email, password="strong-password"):
    """Register a user and return the headers for a valid access token."""
    client.post("/auth/signup", json={"email": email, "password": password})
    response = client.post("/auth/login", json={"email": email, "password": password})

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _profile_form(email: str, **overrides) -> dict:
    """Build a valid multipart profile payload, allowing field overrides."""
    data = {
        "username": "newuser",
        "about": "Hello there",
        "firstName": "John",
        "lastName": "Doe",
        "email": email,
        "country": "United States",
        "streetAddress": "Street 1",
        "city": "City",
        "region": "Region",
        "postalCode": "12345",
        "comments": True,
        "candidates": False,
        "offers": False,
        "push": "everything",
    }
    data.update(overrides)
    return data


def _create_profile_via_service(db_session, current_user, email="profile@example.com", **overrides):
    """Invoke the profile service with a complete, valid set of arguments."""
    values = {
        "username": "newuser",
        "about": "Hello there",
        "first_name": "John",
        "last_name": "Doe",
        "email": email,
        "country": "United States",
        "street_address": "Street 1",
        "city": "City",
        "region": "Region",
        "postal_code": "12345",
        "notify_comments": True,
        "notify_candidates": False,
        "notify_offers": False,
        "push_notifications": PushNotifications.everything,
        "photo": None,
        "cover_photo": None,
    }
    values.update(overrides)
    return profile_service.create_or_update_profile(db_session, current_user=current_user, **values)


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
    assert profile_repository.get_profile_by_id(db_session, 9999) is None


def test_profile_repository_deletes_profile(db_session):
    """Deleting a profile must remove it from the database."""
    profile = _persist_profile(db_session)
    profile_id = profile.id

    profile_repository.delete_profile(db_session, profile)

    assert profile_repository.get_profile_by_id(db_session, profile_id) is None
    assert profile_repository.get_profile_by_email(db_session, "profile@example.com") is None


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


def test_service_get_profile_rejects_invalid_email(db_session):
    """Malformed email input must be rejected before any lookup."""
    with pytest.raises(HTTPException) as exc_info:
        profile_service.get_profile(db_session, "not-an-email", _make_user("profile@example.com"))

    assert exc_info.value.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert exc_info.value.detail == "Invalid email address"


def test_service_get_profile_translates_unexpected_repository_error(db_session, monkeypatch):
    """Unexpected persistence failures must not leak internal details."""

    def _boom(*args, **kwargs):
        raise RuntimeError("database exploded")

    monkeypatch.setattr(profile_repository, "get_profile_by_email", _boom)

    with pytest.raises(HTTPException) as exc_info:
        profile_service.get_profile(db_session, "profile@example.com", _make_user("profile@example.com"))

    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc_info.value.detail == "Unable to retrieve profile"
    assert "database exploded" not in exc_info.value.detail


def test_service_get_user_name_by_email_returns_names_for_owner(db_session):
    """The owner must receive the expected display-name payload."""
    _persist_profile(db_session)

    response = profile_service.get_user_name_by_email(
        db_session, "profile@example.com", _make_user("profile@example.com")
    )

    assert response == {
        "email": "profile@example.com",
        "firstName": "John",
        "lastName": "Doe",
    }


def test_service_get_user_name_by_email_returns_404_when_missing(db_session):
    """A valid email without a profile must surface a not found error."""
    with pytest.raises(HTTPException) as exc_info:
        profile_service.get_user_name_by_email(
            db_session, "ghost@example.com", _make_user("ghost@example.com")
        )

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "User not found"


def test_service_get_user_name_by_email_rejects_other_user(db_session):
    """Cross-user display-name reads must be forbidden."""
    _persist_profile(db_session)

    with pytest.raises(HTTPException) as exc_info:
        profile_service.get_user_name_by_email(
            db_session, "profile@example.com", _make_user("student@example.com")
        )

    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc_info.value.detail == "Not authorized to access this resource"


def test_service_get_user_name_by_email_rejects_invalid_email(db_session):
    """Malformed email input must be rejected with a validation error."""
    with pytest.raises(HTTPException) as exc_info:
        profile_service.get_user_name_by_email(
            db_session, "not-an-email", _make_user("profile@example.com")
        )

    assert exc_info.value.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert exc_info.value.detail == "Invalid email address"


def test_service_get_user_name_by_email_translates_unexpected_error(db_session, monkeypatch):
    """Unexpected persistence failures must not leak internal details."""

    def _boom(*args, **kwargs):
        raise RuntimeError("database exploded")

    monkeypatch.setattr(profile_repository, "get_profile_by_email", _boom)

    with pytest.raises(HTTPException) as exc_info:
        profile_service.get_user_name_by_email(
            db_session, "profile@example.com", _make_user("profile@example.com")
        )

    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc_info.value.detail == "Unable to retrieve profile"
    assert "database exploded" not in exc_info.value.detail


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


def test_service_create_or_update_profile_rejects_invalid_email(db_session):
    """Profile creation must reject malformed email addresses."""
    with pytest.raises(HTTPException) as exc_info:
        _create_profile_via_service(
            db_session,
            _make_user("profile@example.com"),
            email="not-an-email",
        )

    assert exc_info.value.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert exc_info.value.detail == "Invalid email address"


def test_service_create_or_update_profile_rejects_other_user_without_id(db_session):
    """Creating a profile for another user must be forbidden."""
    attacker = _make_user("attacker@example.com")

    with pytest.raises(HTTPException) as exc_info:
        _create_profile_via_service(db_session, attacker, email="profile@example.com")

    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc_info.value.detail == "Not authorized to update this profile"


def test_service_create_or_update_profile_returns_404_for_missing_profile_id(db_session):
    """Updating a non-existent profile id must surface a not found error."""
    with pytest.raises(HTTPException) as exc_info:
        _create_profile_via_service(
            db_session,
            _make_user("profile@example.com"),
            profile_id=9999,
        )

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Profile not found"


def test_service_delete_profile_removes_owned_profile(db_session):
    """The owner must be able to delete their profile."""
    profile = _persist_profile(db_session)

    response = profile_service.delete_profile(
        db_session, profile.id, _make_user("profile@example.com")
    )

    assert response == {"message": "Profile deleted successfully"}
    assert profile_repository.get_profile_by_id(db_session, profile.id) is None


def test_service_delete_profile_returns_404_when_missing(db_session):
    """Deleting a missing profile must surface a not found error."""
    with pytest.raises(HTTPException) as exc_info:
        profile_service.delete_profile(db_session, 9999, _make_user("profile@example.com"))

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Profile not found"


def test_service_delete_profile_rejects_other_user(db_session):
    """Cross-user profile deletion must be forbidden and leave the profile intact."""
    profile = _persist_profile(db_session)

    with pytest.raises(HTTPException) as exc_info:
        profile_service.delete_profile(db_session, profile.id, _make_user("attacker@example.com"))

    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc_info.value.detail == "Not authorized to delete this profile"
    assert profile_repository.get_profile_by_id(db_session, profile.id) is not None


def test_service_delete_profile_translates_unexpected_error(db_session, monkeypatch):
    """Unexpected persistence failures during deletion must return a 500."""
    profile = _persist_profile(db_session)

    def _boom(*args, **kwargs):
        raise RuntimeError("database exploded")

    monkeypatch.setattr(profile_repository, "delete_profile", _boom)

    with pytest.raises(HTTPException) as exc_info:
        profile_service.delete_profile(
            db_session, profile.id, _make_user("profile@example.com")
        )

    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc_info.value.detail == "Unable to delete profile"
    assert "database exploded" not in exc_info.value.detail


# ---------------- API: CRUD, AUTHORIZATION AND RESPONSE VALIDATION ----------------
def test_http_profile_crud_lifecycle(client):
    """Create, retrieve, update and delete a profile through the API."""
    auth = _register_and_authenticate(client, "profile@example.com")

    created = client.post(
        "/profiles/",
        data=_profile_form("profile@example.com"),
        headers=auth,
    )
    assert created.status_code == status.HTTP_201_CREATED
    body = created.json()
    assert set(body) == {
        "id",
        "username",
        "about",
        "firstName",
        "lastName",
        "email",
        "country",
        "streetAddress",
        "city",
        "region",
        "postalCode",
        "notifications",
        "photo",
        "coverPhoto",
    }
    assert isinstance(body["id"], int)
    assert body["username"] == "newuser"
    assert body["firstName"] == "John"
    assert body["lastName"] == "Doe"
    assert body["email"] == "profile@example.com"
    assert body["notifications"] == {
        "comments": True,
        "candidates": False,
        "offers": False,
        "push": "everything",
    }
    assert "hashed_password" not in created.text

    profile_id = body["id"]

    fetched = client.get(
        "/profiles/", params={"email": "profile@example.com"}, headers=auth
    )
    assert fetched.status_code == status.HTTP_200_OK
    assert fetched.json()["id"] == profile_id
    assert fetched.json()["email"] == "profile@example.com"

    names = client.get(
        "/profiles/by-email", params={"email": "profile@example.com"}, headers=auth
    )
    assert names.status_code == status.HTTP_200_OK
    assert names.json() == {
        "email": "profile@example.com",
        "firstName": "John",
        "lastName": "Doe",
    }

    updated = client.put(
        f"/profiles/{profile_id}",
        data=_profile_form(
            "profile@example.com",
            username="updateduser",
            about="Updated about",
            firstName="Jane",
            streetAddress="Street 2",
            postalCode="67890",
            comments=False,
            candidates=True,
            offers=True,
            push="none",
        ),
        headers=auth,
    )
    assert updated.status_code == status.HTTP_200_OK
    assert updated.json()["username"] == "updateduser"
    assert updated.json()["firstName"] == "Jane"
    assert updated.json()["about"] == "Updated about"
    assert updated.json()["postalCode"] == "67890"
    assert updated.json()["notifications"]["comments"] is False
    assert updated.json()["notifications"]["push"] == "none"

    refetched = client.get(
        "/profiles/", params={"email": "profile@example.com"}, headers=auth
    )
    assert refetched.status_code == status.HTTP_200_OK
    assert refetched.json()["username"] == "updateduser"

    deleted = client.delete(f"/profiles/{profile_id}", headers=auth)
    assert deleted.status_code == status.HTTP_200_OK
    assert deleted.json() == {"message": "Profile deleted successfully"}

    missing = client.get(
        "/profiles/", params={"email": "profile@example.com"}, headers=auth
    )
    assert missing.status_code == status.HTTP_404_NOT_FOUND
    assert missing.json()["detail"] == "Profile not found"

    missing_names = client.get(
        "/profiles/by-email", params={"email": "profile@example.com"}, headers=auth
    )
    assert missing_names.status_code == status.HTTP_404_NOT_FOUND
    assert missing_names.json()["detail"] == "User not found"


def test_http_profile_create_rejects_invalid_email(client):
    """The API must reject malformed emails during profile creation."""
    auth = _register_and_authenticate(client, "profile@example.com")

    response = client.post(
        "/profiles/",
        data=_profile_form("not-an-email"),
        headers=auth,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_http_profile_get_rejects_invalid_email(client):
    """The API must reject malformed emails on profile retrieval."""
    auth = _register_and_authenticate(client, "profile@example.com")

    response = client.get("/profiles/", params={"email": "not-an-email"}, headers=auth)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_http_profile_by_email_rejects_invalid_email(client):
    """The API must reject malformed emails on display-name retrieval."""
    auth = _register_and_authenticate(client, "profile@example.com")

    response = client.get(
        "/profiles/by-email", params={"email": "not-an-email"}, headers=auth
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_http_profile_get_missing_returns_404(client):
    """A user without a profile must receive a not found response."""
    auth = _register_and_authenticate(client, "profile@example.com")

    response = client.get(
        "/profiles/", params={"email": "profile@example.com"}, headers=auth
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Profile not found"


def test_http_profile_update_missing_returns_404(client):
    """Updating a non-existent profile id must return 404."""
    auth = _register_and_authenticate(client, "profile@example.com")

    response = client.put(
        "/profiles/9999",
        data=_profile_form("profile@example.com"),
        headers=auth,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Profile not found"


def test_http_profile_delete_other_user_returns_403(client):
    """Users must not be able to delete another user's profile."""
    owner_auth = _register_and_authenticate(client, "owner@example.com")
    created = client.post(
        "/profiles/", data=_profile_form("owner@example.com"), headers=owner_auth
    )
    assert created.status_code == status.HTTP_201_CREATED
    profile_id = created.json()["id"]

    attacker_auth = _register_and_authenticate(client, "attacker@example.com")

    response = client.delete(f"/profiles/{profile_id}", headers=attacker_auth)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Not authorized to delete this profile"

    still_there = client.get(
        "/profiles/", params={"email": "owner@example.com"}, headers=owner_auth
    )
    assert still_there.status_code == status.HTTP_200_OK


def test_http_profile_delete_missing_returns_404(client):
    """Deleting a non-existent profile must return 404."""
    auth = _register_and_authenticate(client, "profile@example.com")

    response = client.delete("/profiles/9999", headers=auth)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Profile not found"


def test_http_profile_delete_requires_authentication(client):
    """Profile deletion must require a valid bearer token."""
    response = client.delete("/profiles/1")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_http_profile_by_email_other_user_returns_403(client):
    """Users must not be able to read another user's display names."""
    owner_auth = _register_and_authenticate(client, "owner@example.com")
    created = client.post(
        "/profiles/", data=_profile_form("owner@example.com"), headers=owner_auth
    )
    assert created.status_code == status.HTTP_201_CREATED

    attacker_auth = _register_and_authenticate(client, "attacker@example.com")

    response = client.get(
        "/profiles/by-email", params={"email": "owner@example.com"}, headers=attacker_auth
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Not authorized to access this resource"
