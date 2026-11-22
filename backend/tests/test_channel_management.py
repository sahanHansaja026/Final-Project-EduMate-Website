"""Tests for the channel management API implemented by Issue #24 Phase 1."""

from fastapi import status


def _register_user(client, email: str, password: str = "strong-password"):
    """Register a user and return their id with valid bearer headers."""
    signup_response = client.post(
        "/auth/signup",
        json={"email": email, "password": password},
    )
    assert signup_response.status_code == status.HTTP_201_CREATED

    user_id = signup_response.json()["user_id"]
    login_response = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    token = login_response.json()["access_token"]

    return user_id, {"Authorization": f"Bearer {token}"}


def _create_channel(
    client,
    auth: dict,
    user_id: int,
    channel_name: str = "Test Channel",
):
    """Create a channel as the authenticated owner."""
    response = client.post(
        "/channels/",
        data={
            "user_id": user_id,
            "channel_name": channel_name,
            "description": "Channel used by automated tests",
            "institute_legal_name": "Test Institute",
            "institute_owner_full_name": "Test Owner",
            "physical_corporate_address": "Test Address",
            "co_hosts_and_faculty_members": "[]",
            "visibility": "public",
            "official_website_link": "",
            "facebook_portal_link": "",
        },
        headers=auth,
    )

    assert response.status_code == status.HTTP_200_OK
    return response.json()


def test_create_channel_requires_authentication(client):
    response = client.post(
        "/channels/",
        data={
            "user_id": 1,
            "channel_name": "Unauthorized Channel",
            "institute_legal_name": "Test Institute",
            "institute_owner_full_name": "Test Owner",
            "co_hosts_and_faculty_members": "[]",
            "visibility": "public",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_owner_can_create_and_retrieve_channel(client):
    owner_id, auth = _register_user(client, "student@example.com")

    created = _create_channel(client, auth, owner_id, "Owner Channel")
    channel_id = created["channel_id"]

    retrieved = client.get(f"/channels/{channel_id}")

    assert retrieved.status_code == status.HTTP_200_OK
    assert retrieved.json()["channel_id"] == channel_id
    assert retrieved.json()["channel_name"] == "Owner Channel"
    assert retrieved.json()["user_id"] == owner_id


def test_owner_can_update_channel(client):
    owner_id, auth = _register_user(client, "owner-update-channel@example.com")
    created = _create_channel(client, auth, owner_id, "Before Update")
    channel_id = created["channel_id"]

    response = client.put(
        f"/channels/{channel_id}",
        data={
            "user_id": owner_id,
            "channel_name": "After Update",
            "description": "Updated description",
            "institute_legal_name": "Updated Institute",
            "institute_owner_full_name": "Updated Owner",
            "physical_corporate_address": "Updated Address",
            "co_hosts_and_faculty_members": "[]",
            "visibility": "private",
            "official_website_link": "",
            "facebook_portal_link": "",
        },
        headers=auth,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["channel_name"] == "After Update"
    assert response.json()["visibility"] == "private"


def test_owner_can_delete_channel(client):
    owner_id, auth = _register_user(client, "owner-delete-channel@example.com")
    created = _create_channel(client, auth, owner_id, "Temporary Channel")
    channel_id = created["channel_id"]

    response = client.delete(
        f"/channels/{channel_id}",
        params={"user_id": owner_id},
        headers=auth,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Channel and its linked cloud assets deleted successfully"


def test_unauthenticated_user_cannot_update_or_delete_channel(client):
    owner_id, auth = _register_user(client, "owner-protected-channel@example.com")
    created = _create_channel(client, auth, owner_id, "Protected Channel")
    channel_id = created["channel_id"]

    attacker_id, attacker_auth = _register_user(
        client,
        "attacker-protected-channel@example.com",
    )

    update_response = client.put(
        f"/channels/{channel_id}",
        data={
            "user_id": attacker_id,
            "channel_name": "Attempted Hijack",
            "institute_legal_name": "Test Institute",
            "institute_owner_full_name": "Test Owner",
            "co_hosts_and_faculty_members": "[]",
            "visibility": "private",
        },
        headers=attacker_auth,
    )
    assert update_response.status_code == status.HTTP_403_FORBIDDEN

    update_impersonation_response = client.put(
        f"/channels/{channel_id}",
        data={
            "user_id": owner_id,
            "channel_name": "Attempted Hijack",
            "institute_legal_name": "Test Institute",
            "institute_owner_full_name": "Test Owner",
            "co_hosts_and_faculty_members": "[]",
            "visibility": "private",
        },
        headers=attacker_auth,
    )
    assert update_impersonation_response.status_code == status.HTTP_403_FORBIDDEN

    delete_response = client.delete(
        f"/channels/{channel_id}",
        params={"user_id": attacker_id},
        headers=attacker_auth,
    )
    assert delete_response.status_code == status.HTTP_403_FORBIDDEN

    delete_impersonation_response = client.delete(
        f"/channels/{channel_id}",
        params={"user_id": owner_id},
        headers=attacker_auth,
    )
    assert delete_impersonation_response.status_code == status.HTTP_403_FORBIDDEN


def test_missing_channel_returns_404(client):
    owner_id, auth = _register_user(client, "owner-missing-channel@example.com")

    missing_response = client.get("/channels/999999")
    assert missing_response.status_code == status.HTTP_404_NOT_FOUND
    assert missing_response.json()["detail"] == "Channel not found"

    missing_update_response = client.put(
        "/channels/999999",
        data={
            "user_id": owner_id,
            "channel_name": "Missing",
            "institute_legal_name": "Test Institute",
            "institute_owner_full_name": "Test Owner",
            "co_hosts_and_faculty_members": "[]",
            "visibility": "public",
        },
        headers=auth,
    )
    assert missing_update_response.status_code == status.HTTP_404_NOT_FOUND

    missing_delete_response = client.delete(
        "/channels/999999",
        params={"user_id": owner_id},
        headers=auth,
    )
    assert missing_delete_response.status_code == status.HTTP_404_NOT_FOUND
