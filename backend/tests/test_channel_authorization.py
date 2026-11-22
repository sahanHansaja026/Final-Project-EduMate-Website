"""Authorization and co-host tests for the channel management API."""

from fastapi import status

from app.models.channel import Channel
from app.models.channel_modules import ChannelModule, VisibilityEnum


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
    co_hosts_json: str,
    channel_name: str = "Co-host Channel",
):
    response = client.post(
        "/channels/",
        data={
            "user_id": user_id,
            "channel_name": channel_name,
            "description": "Channel used for co-host authorization tests",
            "institute_legal_name": "Test Institute",
            "institute_owner_full_name": "Test Owner",
            "physical_corporate_address": "Test Address",
            "co_hosts_and_faculty_members": co_hosts_json,
            "visibility": "public",
            "official_website_link": "",
            "facebook_portal_link": "",
        },
        headers=auth,
    )

    assert response.status_code == status.HTTP_200_OK
    return response.json(), user_id


def _create_module(
    db_session,
    channel_id: int,
    owner_id: int,
    co_host_email: str,
):
    module = ChannelModule(
        channel_id=channel_id,
        user_id=owner_id,
        name="Co-host Module",
        description="Module managed through co-host authorization",
        co_host_email=co_host_email,
        visibility=VisibilityEnum.public,
    )
    db_session.add(module)
    db_session.commit()
    db_session.refresh(module)
    return module


def test_valid_co_host_can_authorize_and_manage_module_students(
    client,
    db_session,
):
    owner_id, owner_auth = _register_user(client, "cohost-owner@example.com")
    cohost_id, cohost_auth = _register_user(client, "cohost@example.com")

    created, owner_record_id = _create_channel(
        client,
        owner_auth,
        owner_id,
        '["cohost@example.com"]',
        "Valid Co-host Channel",
    )
    channel_id = created["channel_id"]
    module = _create_module(
        db_session,
        channel_id=channel_id,
        owner_id=owner_record_id,
        co_host_email="cohost@example.com",
    )

    authorization_response = client.get(
        f"/channels/{channel_id}/authorize",
        params={
            "current_user_id": cohost_id,
            "current_email": "cohost@example.com",
        },
        headers=cohost_auth,
    )
    assert authorization_response.status_code == status.HTTP_200_OK
    assert authorization_response.json()["authorized"] is True
    assert authorization_response.json()["role"] == "co_host"

    student_response = client.post(
        "/authorized-students/",
        json={
            "channel_module_id": module.module_id,
            "student_name": "Authorized Student",
            "student_email": "student@cohost.example",
            "status": "active",
            "remark": None,
        },
        headers=cohost_auth,
    )
    assert student_response.status_code == status.HTTP_200_OK
    assert student_response.json()["channel_module_id"] == module.module_id


def test_co_host_cannot_update_or_delete_channel(client):
    owner_id, owner_auth = _register_user(client, "cohost-owner-only@example.com")
    cohost_id, cohost_auth = _register_user(client, "cohost-only@example.com")

    created, _ = _create_channel(
        client,
        owner_auth,
        owner_id,
        '["cohost-only@example.com"]',
        "Co-host Owner-Only Channel",
    )
    channel_id = created["channel_id"]

    update_response = client.put(
        f"/channels/{channel_id}",
        data={
            "user_id": cohost_id,
            "channel_name": "Co-host Attempt",
        },
        headers=cohost_auth,
    )
    assert update_response.status_code == status.HTTP_403_FORBIDDEN

    delete_response = client.delete(
        f"/channels/{channel_id}",
        params={"user_id": cohost_id},
        headers=cohost_auth,
    )
    assert delete_response.status_code == status.HTTP_403_FORBIDDEN


def test_legacy_dictionary_based_co_host_entries_are_supported(
    client,
    db_session,
):
    owner_id, owner_auth = _register_user(client, "legacy-cohost-owner@example.com")
    legacy_cohost_id, legacy_cohost_auth = _register_user(
        client,
        "legacy-cohost@example.com",
    )

    created, _ = _create_channel(
        client,
        owner_auth,
        owner_id,
        "[]",
        "Legacy Co-host Channel",
    )
    channel_id = created["channel_id"]

    channel = db_session.query(Channel).filter(Channel.channel_id == channel_id).one()
    channel.co_hosts_and_faculty_members = [
        {"email": "legacy-cohost@example.com"}
    ]
    db_session.commit()

    authorization_response = client.get(
        f"/channels/{channel_id}/authorize",
        params={
            "current_user_id": legacy_cohost_id,
            "current_email": "legacy-cohost@example.com",
        },
        headers=legacy_cohost_auth,
    )

    assert authorization_response.status_code == status.HTTP_200_OK
    assert authorization_response.json()["authorized"] is True
    assert authorization_response.json()["role"] == "co_host"


def test_invalid_co_host_identity_is_rejected(client):
    owner_id, owner_auth = _register_user(client, "invalid-cohost-owner@example.com")
    invalid_user_id, invalid_user_auth = _register_user(
        client,
        "invalid-cohost-user@example.com",
    )

    created, _ = _create_channel(
        client,
        owner_auth,
        owner_id,
        "[]",
        "Invalid Co-host Channel",
    )
    channel_id = created["channel_id"]

    authorization_response = client.get(
        f"/channels/{channel_id}/authorize",
        params={
            "current_user_id": invalid_user_id,
            "current_email": "invalid-cohost-user@example.com",
        },
        headers=invalid_user_auth,
    )
    assert authorization_response.status_code == status.HTTP_200_OK
    assert authorization_response.json()["authorized"] is False
    assert authorization_response.json()["role"] is None

    student_response = client.post(
        "/authorized-students/",
        json={
            "channel_module_id": 999999,
            "student_name": "Unauthorized Student",
            "student_email": "unauthorized-student@example.com",
            "status": "active",
            "remark": None,
        },
        headers=invalid_user_auth,
    )
    assert student_response.status_code == status.HTTP_404_NOT_FOUND
