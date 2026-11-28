"""Analytics and authorization tests for the channel management API."""

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


def _create_channel(client, auth: dict, user_id: int, channel_name: str):
    response = client.post(
        "/channels/",
        data={
            "user_id": user_id,
            "channel_name": channel_name,
            "description": "Channel used for analytics tests",
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


def test_owner_can_access_channel_analytics(client):
    owner_id, owner_auth = _register_user(client, "analytics-owner@example.com")
    created = _create_channel(client, owner_auth, owner_id, "Analytics Channel")
    channel_id = created["channel_id"]

    response = client.get(
        f"/channel-analytics/{owner_id}",
        headers=owner_auth,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["user_id"] == owner_id
    assert response.json()["channels_count"] == 1
    assert response.json()["channels"][0]["channel_id"] == channel_id
    assert response.json()["channels"][0]["modules_count"] == 0
    assert response.json()["channels"][0]["total_students"] == 0


def test_authenticated_user_cannot_access_another_users_analytics(client):
    owner_id, owner_auth = _register_user(client, "analytics-owner-2@example.com")
    created = _create_channel(client, owner_auth, owner_id, "Private Analytics Channel")
    attacker_id, attacker_auth = _register_user(
        client,
        "analytics-attacker@example.com",
    )

    owner_to_attacker_response = client.get(
        f"/channel-analytics/{attacker_id}",
        headers=owner_auth,
    )
    attacker_to_owner_response = client.get(
        f"/channel-analytics/{owner_id}",
        headers=attacker_auth,
    )

    assert owner_to_attacker_response.status_code == status.HTTP_403_FORBIDDEN
    assert attacker_to_owner_response.status_code == status.HTTP_403_FORBIDDEN


def test_malformed_or_manipulated_analytics_user_id_is_rejected(client):
    owner_id, owner_auth = _register_user(client, "analytics-owner-3@example.com")
    created = _create_channel(client, owner_auth, owner_id, "Manipulated Analytics Channel")
    channel_id = created["channel_id"]
    attacker_id, attacker_auth = _register_user(
        client,
        "analytics-attacker-2@example.com",
    )

    mismatched_owner_response = client.get(
        f"/channel-analytics/{owner_id}",
        params={"current_user_id": attacker_id},
        headers=owner_auth,
    )
    mismatched_attacker_response = client.get(
        f"/channel-analytics/{attacker_id}",
        params={"current_user_id": owner_id},
        headers=attacker_auth,
    )

    assert mismatched_owner_response.status_code == status.HTTP_403_FORBIDDEN
    assert mismatched_attacker_response.status_code == status.HTTP_403_FORBIDDEN
    assert channel_id is not None


def test_analytics_returns_only_authenticated_users_own_channels(client):
    owner_id, owner_auth = _register_user(client, "analytics-owner-4@example.com")
    created_by_owner = _create_channel(
        client,
        owner_auth,
        owner_id,
        "Owner Analytics Channel",
    )
    attacker_id, attacker_auth = _register_user(
        client,
        "analytics-attacker-3@example.com",
    )
    created_by_attacker = _create_channel(
        client,
        attacker_auth,
        attacker_id,
        "Attacker Analytics Channel",
    )

    owner_response = client.get(
        f"/channel-analytics/{owner_id}",
        headers=owner_auth,
    )
    attacker_response = client.get(
        f"/channel-analytics/{attacker_id}",
        headers=attacker_auth,
    )

    assert owner_response.status_code == status.HTTP_200_OK
    assert attacker_response.status_code == status.HTTP_200_OK
    assert owner_response.json()["channels_count"] == 1
    assert owner_response.json()["channels"][0]["channel_id"] == created_by_owner["channel_id"]
    assert attacker_response.json()["channels_count"] == 1
    assert attacker_response.json()["channels"][0]["channel_id"] == created_by_attacker["channel_id"]


def test_cross_user_analytics_error_detail_is_stable(client):
    owner_id, owner_auth = _register_user(client, "analytics-error-detail-owner@example.com")
    attacker_id, _attacker_auth = _register_user(client, "analytics-error-detail-attacker@example.com")

    response = client.get(f"/channel-analytics/{attacker_id}", headers=owner_auth)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Not authorized to view another user's channel analytics"


def test_missing_analytics_resources_are_handled_safely(client):
    user_id, auth = _register_user(client, "analytics-owner-no-channels@example.com")

    response = client.get(
        f"/channel-analytics/{user_id}",
        headers=auth,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["user_id"] == user_id
    assert response.json()["channels_count"] == 0
    assert response.json()["channels"] == []


def test_analytics_requires_authentication(client):
    response = client.get("/channel-analytics/1")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    invalid_token_response = client.get(
        "/channel-analytics/1",
        headers={"Authorization": "Bearer not-a-valid-token"},
    )
    assert invalid_token_response.status_code == status.HTTP_401_UNAUTHORIZED


def test_invalid_analytics_user_identifier_returns_validation_error(client):
    _user_id, auth = _register_user(client, "analytics-invalid-user-id@example.com")

    response = client.get("/channel-analytics/not-an-integer", headers=auth)

    assert response.status_code == 422
