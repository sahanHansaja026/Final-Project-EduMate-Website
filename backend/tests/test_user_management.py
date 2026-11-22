"""Tests for the user management module (user accounts + profiles)."""

from app.models.profile import Profile
from app.models.subscription import Subscription
from app.models.user import User


def _register_and_authenticate(client, email, password="strong-password"):
    """Register a user and return the headers for a valid access token."""
    client.post("/auth/signup", json={"email": email, "password": password})
    response = client.post("/auth/login", json={"email": email, "password": password})

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_signup_creates_user_and_provisions_free_subscription(client, db_session):
    response = client.post(
        "/auth/signup",
        json={"email": "student@example.com", "password": "strong-password"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["message"] == "User registered successfully"
    assert body["user_id"] is not None

    user = db_session.query(User).filter(User.email == "student@example.com").one()
    assert user.email == "student@example.com"
    assert user.hashed_password != "strong-password"

    subscription = (
        db_session.query(Subscription).filter(Subscription.user_id == user.user_id).first()
    )
    assert subscription is not None


def test_signup_duplicate_email_returns_400(client):
    first = client.post(
        "/auth/signup",
        json={"email": "student@example.com", "password": "strong-password"},
    )
    assert first.status_code == 201

    second = client.post(
        "/auth/signup",
        json={"email": "student@example.com", "password": "strong-password"},
    )

    assert second.status_code == 400
    assert second.json()["detail"] == "Email already exists"


def test_signup_response_never_contains_password_data(client):
    response = client.post(
        "/auth/signup",
        json={"email": "student@example.com", "password": "strong-password"},
    )

    assert response.status_code == 201
    assert "hashed_password" not in response.text
    assert "strong-password" not in response.text


def test_login_with_valid_credentials_returns_tokens(client, db_session):
    client.post(
        "/auth/signup",
        json={"email": "student@example.com", "password": "strong-password"},
    )

    response = client.post(
        "/auth/login",
        json={"email": "student@example.com", "password": "strong-password"},
    )

    assert response.status_code == 200

    from app.schemas.user import TokenSchema

    token = TokenSchema(**response.json())
    assert token.token_type == "bearer"
    assert token.user.email == "student@example.com"
    assert token.user.id is not None
    assert "hashed_password" not in response.text


def test_login_with_wrong_password_returns_401(client):
    client.post(
        "/auth/signup",
        json={"email": "student@example.com", "password": "strong-password"},
    )

    response = client.post(
        "/auth/login",
        json={"email": "student@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_with_unknown_email_returns_401(client):
    response = client.post(
        "/auth/login",
        json={"email": "ghost@example.com", "password": "strong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_logout_with_valid_refresh_token_clears_session(client, db_session):
    client.post(
        "/auth/signup",
        json={"email": "student@example.com", "password": "strong-password"},
    )

    login_response = client.post(
        "/auth/login",
        json={"email": "student@example.com", "password": "strong-password"},
    )
    refresh_token = login_response.json()["refresh_token"]

    logout_response = client.post("/auth/logout", params={"refresh_token": refresh_token})

    assert logout_response.status_code == 200
    assert logout_response.json()["message"] == "Logged out successfully"

    user = db_session.query(User).filter(User.email == "student@example.com").one()
    assert user.refresh_token is None


def test_logout_with_unknown_refresh_token_returns_401(client):
    response = client.post("/auth/logout", params={"refresh_token": "not-a-real-token"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


# ---------------- USER PROFILE: RETRIEVE / UPDATE ----------------
def test_create_profile_returns_created_profile(client):
    auth = _register_and_authenticate(client, "profile@example.com")

    response = client.post(
        "/profiles/",
        data={
            "username": "newuser",
            "about": "Hello there",
            "firstName": "John",
            "lastName": "Doe",
            "email": "profile@example.com",
            "country": "United States",
            "streetAddress": "Street 1",
            "city": "City",
            "region": "Region",
            "postalCode": "12345",
            "comments": True,
            "candidates": False,
            "offers": False,
            "push": "everything",
        },
        headers=auth,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "newuser"
    assert body["firstName"] == "John"
    assert body["lastName"] == "Doe"
    assert body["email"] == "profile@example.com"
    assert body["notifications"]["comments"] is True
    assert "hashed_password" not in response.text


def test_get_profile_by_email_returns_names(client):
    auth = _register_and_authenticate(client, "profile@example.com")

    response = client.get("/profiles/by-email", params={"email": "profile@example.com"}, headers=auth)

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_profile_returns_profile_or_404(client):
    auth = _register_and_authenticate(client, "profile@example.com")

    created = client.post(
        "/profiles/",
        data={
            "username": "newuser",
            "about": "Hello there",
            "firstName": "John",
            "lastName": "Doe",
            "email": "profile@example.com",
            "country": "United States",
            "streetAddress": "Street 1",
            "city": "City",
            "region": "Region",
            "postalCode": "12345",
            "comments": True,
            "candidates": False,
            "offers": False,
            "push": "everything",
        },
        headers=auth,
    )
    assert created.status_code == 201

    found = client.get("/profiles/", params={"email": "profile@example.com"}, headers=auth)

    assert found.status_code == 200
    assert found.json()["email"] == "profile@example.com"

    stranger_auth = _register_and_authenticate(client, "student@example.com")
    missing = client.get("/profiles/", params={"email": "student@example.com"}, headers=stranger_auth)

    assert missing.status_code == 404
    assert missing.json()["detail"] == "Profile not found"


def test_update_profile_changes_stored_fields(client, db_session):
    auth = _register_and_authenticate(client, "profile@example.com")

    client.post(
        "/profiles/",
        data={
            "username": "newuser",
            "about": "Hello there",
            "firstName": "John",
            "lastName": "Doe",
            "email": "profile@example.com",
            "country": "United States",
            "streetAddress": "Street 1",
            "city": "City",
            "region": "Region",
            "postalCode": "12345",
            "comments": True,
            "candidates": False,
            "offers": False,
            "push": "everything",
        },
        headers=auth,
    )

    updated = client.post(
        "/profiles/",
        data={
            "username": "updateduser",
            "about": "Updated about",
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "profile@example.com",
            "country": "United States",
            "streetAddress": "Street 2",
            "city": "City",
            "region": "Region",
            "postalCode": "67890",
            "comments": False,
            "candidates": True,
            "offers": True,
            "push": "none",
        },
        headers=auth,
    )

    assert updated.status_code == 201
    assert updated.json()["username"] == "updateduser"
    assert updated.json()["about"] == "Updated about"

    profile = db_session.query(Profile).filter_by(email="profile@example.com").one()
    assert profile.username == "updateduser"


def test_profile_photo_upload_and_retrieval(client):
    auth = _register_and_authenticate(client, "profile@example.com")

    created = client.post(
        "/profiles/",
        data={
            "username": "newuser",
            "about": "Hello there",
            "firstName": "John",
            "lastName": "Doe",
            "email": "profile@example.com",
            "country": "United States",
            "streetAddress": "Street 1",
            "city": "City",
            "region": "Region",
            "postalCode": "12345",
            "comments": True,
            "candidates": False,
            "offers": False,
            "push": "everything",
        },
        files={"photo": ("photo.jpg", b"fake-image-bytes", "image/jpeg")},
        headers=auth,
    )
    assert created.status_code == 201

    photo_response = client.get("/profiles/photo", params={"email": "profile@example.com"}, headers=auth)

    assert photo_response.status_code == 200
    assert photo_response.content == b"fake-image-bytes"
    assert photo_response.headers["content-type"].startswith("image/jpeg")

    no_photo_auth = _register_and_authenticate(client, "student@example.com")
    missing_response = client.get("/profiles/photo", params={"email": "student@example.com"}, headers=no_photo_auth)

    assert missing_response.status_code == 404
    assert missing_response.json()["detail"] == "Profile photo not found"


# ---------------- VALIDATION ----------------
def test_signup_rejects_invalid_email(client):
    response = client.post(
        "/auth/signup",
        json={"email": "not-an-email", "password": "strong-password"},
    )

    assert response.status_code == 422


def test_signup_requires_password(client):
    response = client.post(
        "/auth/signup",
        json={"email": "student@example.com"},
    )

    assert response.status_code == 422
