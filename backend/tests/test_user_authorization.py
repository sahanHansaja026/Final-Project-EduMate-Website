"""Authorization tests for the user management module."""

import pytest
from fastapi import status


def _register_and_authenticate(client, email, password="strong-password"):
    """Register a user and return the headers for a valid access token."""
    client.post("/auth/signup", json={"email": email, "password": password})
    response = client.post("/auth/login", json={"email": email, "password": password})

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _create_profile(client, auth, email, username="newuser"):
    return client.post(
        "/profiles/",
        data={
            "username": username,
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
        },
        headers=auth,
    )


def test_get_profile_without_token_returns_401(client):
    response = client.get("/profiles/", params={"email": "student@example.com"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_profile_with_invalid_token_returns_401(client):
    response = client.get(
        "/profiles/",
        params={"email": "student@example.com"},
        headers={"Authorization": "Bearer not-a-valid-token"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_profile_with_valid_token_returns_own_profile(client):
    auth = _register_and_authenticate(client, "student@example.com")
    created = _create_profile(client, auth, "student@example.com", username="ownuser")
    assert created.status_code == 201

    response = client.get("/profiles/", params={"email": "student@example.com"}, headers=auth)

    assert response.status_code == 200
    assert response.json()["username"] == "ownuser"


def test_access_other_users_profile_returns_403(client):
    owner_auth = _register_and_authenticate(client, "owner@example.com")
    created = _create_profile(client, owner_auth, "owner@example.com")
    assert created.status_code == 201

    attacker_auth = _register_and_authenticate(client, "attacker@example.com")

    response = client.get(
        "/profiles/",
        params={"email": "owner@example.com"},
        headers=attacker_auth,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_access_other_users_display_names_returns_403(client):
    owner_auth = _register_and_authenticate(client, "owner@example.com")
    created = _create_profile(client, owner_auth, "owner@example.com")
    assert created.status_code == 201

    attacker_auth = _register_and_authenticate(client, "attacker@example.com")

    response = client.get(
        "/profiles/by-email",
        params={"email": "owner@example.com"},
        headers=attacker_auth,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_access_other_users_profile_photo_returns_403(client):
    owner_auth = _register_and_authenticate(client, "owner@example.com")
    created = _create_profile(client, owner_auth, "owner@example.com")
    assert created.status_code == 201

    attacker_auth = _register_and_authenticate(client, "attacker@example.com")

    response = client.get(
        "/profiles/photo",
        params={"email": "owner@example.com"},
        headers=attacker_auth,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_other_users_profile_returns_403(client):
    owner_auth = _register_and_authenticate(client, "owner@example.com")
    created = _create_profile(client, owner_auth, "owner@example.com")
    assert created.status_code == 201
    original_username = created.json()["username"]

    attacker_auth = _register_and_authenticate(client, "attacker@example.com")

    response = client.post(
        "/profiles/",
        data={
            "username": "hijacked",
            "about": "Malicious update",
            "firstName": "Attacker",
            "lastName": "McAttack",
            "email": "owner@example.com",
            "country": "United States",
            "streetAddress": "Street 1",
            "city": "City",
            "region": "Region",
            "postalCode": "12345",
            "comments": False,
            "candidates": False,
            "offers": False,
            "push": "none",
        },
        headers=attacker_auth,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert created.json()["username"] == original_username


def test_update_other_users_profile_by_id_returns_403(client):
    owner_auth = _register_and_authenticate(client, "owner@example.com")
    created = _create_profile(client, owner_auth, "owner@example.com")
    assert created.status_code == 201
    profile_id = created.json()["id"]

    attacker_auth = _register_and_authenticate(client, "attacker@example.com")

    response = client.put(
        f"/profiles/{profile_id}",
        data={
            "username": "hijacked",
            "about": "Malicious update",
            "firstName": "Attacker",
            "lastName": "McAttack",
            "email": "owner@example.com",
            "country": "United States",
            "streetAddress": "Street 1",
            "city": "City",
            "region": "Region",
            "postalCode": "12345",
            "comments": False,
            "candidates": False,
            "offers": False,
            "push": "none",
        },
        headers=attacker_auth,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
