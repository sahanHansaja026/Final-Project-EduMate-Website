"""Authorized-student management tests for the channel backend."""

from fastapi import status

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


def _create_channel(client, auth: dict, user_id: int, channel_name: str):
    response = client.post(
        "/channels/",
        data={
            "user_id": user_id,
            "channel_name": channel_name,
            "description": "Channel used for authorized-student tests",
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


def _create_module(
    db_session,
    channel_id: int,
    owner_id: int,
    module_name: str = "Authorized Student Module",
):
    module = ChannelModule(
        channel_id=channel_id,
        user_id=owner_id,
        name=module_name,
        description="Module used for authorized-student tests",
        visibility=VisibilityEnum.public,
    )
    db_session.add(module)
    db_session.commit()
    db_session.refresh(module)
    return module


def _add_student(
    client,
    auth: dict,
    module_id: int,
    student_email: str = "authorized-student@example.com",
):
    response = client.post(
        "/authorized-students/",
        json={
            "channel_module_id": module_id,
            "student_name": "Authorized Student",
            "student_email": student_email,
            "status": "active",
            "remark": None,
        },
        headers=auth,
    )
    return response


def test_authorized_user_can_add_get_update_and_delete_student(
    client,
    db_session,
):
    owner_id, owner_auth = _register_user(client, "authorized-owner@example.com")
    created = _create_channel(client, owner_auth, owner_id, "Authorized Student Channel")
    module = _create_module(db_session, created["channel_id"], owner_id)

    add_response = _add_student(client, owner_auth, module.module_id)
    assert add_response.status_code == status.HTTP_200_OK

    get_response = client.get(
        f"/authorized-students/module/{module.module_id}",
        headers=owner_auth,
    )
    assert get_response.status_code == status.HTTP_200_OK
    assert len(get_response.json()) == 1

    student_id = add_response.json()["id"]
    update_response = client.put(
        f"/authorized-students/{student_id}",
        json={"status": "suspend", "remark": "Temporary suspension"},
        headers=owner_auth,
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json()["status"] == "suspend"

    delete_response = client.delete(
        f"/authorized-students/{student_id}",
        headers=owner_auth,
    )
    assert delete_response.status_code == status.HTTP_200_OK
    assert delete_response.json()["message"] == "Student removed successfully"


def test_unauthorized_user_cannot_manage_student_authorization(
    client,
    db_session,
):
    owner_id, owner_auth = _register_user(client, "student-owner@example.com")
    attacker_id, attacker_auth = _register_user(
        client,
        "student-attacker@example.com",
    )
    created = _create_channel(client, owner_auth, owner_id, "Unauthorized Student Channel")
    module = _create_module(db_session, created["channel_id"], owner_id)

    add_response = _add_student(client, owner_auth, module.module_id)
    assert add_response.status_code == status.HTTP_200_OK
    student_id = add_response.json()["id"]

    attacker_add_response = _add_student(
        client,
        attacker_auth,
        module.module_id,
        "another-student@example.com",
    )
    attacker_update_response = client.put(
        f"/authorized-students/{student_id}",
        json={"status": "suspend", "remark": "Unauthorized attempt"},
        headers=attacker_auth,
    )
    attacker_delete_response = client.delete(
        f"/authorized-students/{student_id}",
        headers=attacker_auth,
    )

    assert attacker_add_response.status_code == status.HTTP_403_FORBIDDEN
    assert attacker_update_response.status_code == status.HTTP_403_FORBIDDEN
    assert attacker_delete_response.status_code == status.HTTP_403_FORBIDDEN


def test_cross_channel_module_student_relationship_is_rejected(
    client,
    db_session,
):
    owner_a_id, owner_a_auth = _register_user(client, "cross-owner-a@example.com")
    owner_b_id, owner_b_auth = _register_user(client, "cross-owner-b@example.com")
    created_a = _create_channel(client, owner_a_auth, owner_a_id, "Cross Channel A")
    created_b = _create_channel(client, owner_b_auth, owner_b_id, "Cross Channel B")
    module_a = _create_module(db_session, created_a["channel_id"], owner_a_id)
    module_b = _create_module(db_session, created_b["channel_id"], owner_b_id)

    add_response = _add_student(client, owner_a_auth, module_a.module_id)
    assert add_response.status_code == status.HTTP_200_OK
    student_id = add_response.json()["id"]

    owner_b_update_response = client.put(
        f"/authorized-students/{student_id}",
        json={"status": "suspend", "remark": "Cross-channel attempt"},
        headers=owner_b_auth,
    )
    owner_b_delete_response = client.delete(
        f"/authorized-students/{student_id}",
        headers=owner_b_auth,
    )
    owner_a_add_to_b_response = _add_student(
        client,
        owner_a_auth,
        module_b.module_id,
        "cross-student-b@example.com",
    )

    assert owner_b_update_response.status_code == status.HTTP_403_FORBIDDEN
    assert owner_b_delete_response.status_code == status.HTTP_403_FORBIDDEN
    assert owner_a_add_to_b_response.status_code == status.HTTP_403_FORBIDDEN


def test_duplicate_student_authorization_is_rejected(client, db_session):
    owner_id, owner_auth = _register_user(client, "duplicate-owner@example.com")
    created = _create_channel(client, owner_auth, owner_id, "Duplicate Student Channel")
    module = _create_module(db_session, created["channel_id"], owner_id)

    first_response = _add_student(
        client,
        owner_auth,
        module.module_id,
        "duplicate-student@example.com",
    )
    second_response = _add_student(
        client,
        owner_auth,
        module.module_id,
        "duplicate-student@example.com",
    )

    assert first_response.status_code == status.HTTP_200_OK
    assert second_response.status_code == status.HTTP_400_BAD_REQUEST
    assert second_response.json()["detail"] == "Student is already authorized for this module"


def test_missing_authorized_student_resources_return_404(client, db_session):
    owner_id, owner_auth = _register_user(client, "missing-student-owner@example.com")
    created = _create_channel(client, owner_auth, owner_id, "Missing Student Channel")
    module = _create_module(db_session, created["channel_id"], owner_id)

    missing_module_add_response = _add_student(
        client,
        owner_auth,
        999999,
        "missing-student@example.com",
    )
    missing_module_get_response = client.get(
        "/authorized-students/module/999999",
        headers=owner_auth,
    )
    missing_student_get_response = client.get(
        "/authorized-students/999999",
        headers=owner_auth,
    )
    missing_student_update_response = client.put(
        "/authorized-students/999999",
        json={"status": "suspend", "remark": None},
        headers=owner_auth,
    )
    missing_student_delete_response = client.delete(
        "/authorized-students/999999",
        headers=owner_auth,
    )

    assert missing_module_add_response.status_code == status.HTTP_404_NOT_FOUND
    assert missing_module_get_response.status_code == status.HTTP_404_NOT_FOUND
    assert missing_student_get_response.status_code == status.HTTP_404_NOT_FOUND
    assert missing_student_update_response.status_code == status.HTTP_404_NOT_FOUND
    assert missing_student_delete_response.status_code == status.HTTP_404_NOT_FOUND


def test_orphaned_student_record_can_be_deleted(client, db_session):
    owner_id, owner_auth = _register_user(client, "orphan-owner@example.com")
    created = _create_channel(client, owner_auth, owner_id, "Orphan Student Channel")
    module = _create_module(db_session, created["channel_id"], owner_id)

    add_response = _add_student(client, owner_auth, module.module_id)
    assert add_response.status_code == status.HTTP_200_OK
    student_id = add_response.json()["id"]

    db_session.query(ChannelModule).filter(
        ChannelModule.module_id == module.module_id,
    ).delete()
    db_session.commit()

    delete_response = client.delete(
        f"/authorized-students/{student_id}",
        headers=owner_auth,
    )
    assert delete_response.status_code == status.HTTP_200_OK
    assert delete_response.json()["message"] == "Student removed successfully"
