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


def test_authorized_student_endpoints_require_authentication(client, db_session):
    """Anonymous and invalid-token callers cannot reach student endpoints."""
    owner_id, owner_auth = _register_user(client, "auth-protected-owner@example.com")
    created = _create_channel(client, owner_auth, owner_id, "Auth Protected Channel")
    module = _create_module(db_session, created["channel_id"], owner_id)

    add_response = _add_student(client, owner_auth, module.module_id)
    assert add_response.status_code == status.HTTP_200_OK
    student_id = add_response.json()["id"]

    anonymous_module_response = client.get(f"/authorized-students/module/{module.module_id}")
    anonymous_student_response = client.get(f"/authorized-students/{student_id}")
    anonymous_add_response = client.post(
        "/authorized-students/",
        json={
            "channel_module_id": module.module_id,
            "student_name": "Anonymous Student",
            "student_email": "anonymous-student@example.com",
            "status": "active",
            "remark": None,
        },
    )
    anonymous_update_response = client.put(
        f"/authorized-students/{student_id}",
        json={"status": "suspend", "remark": None},
    )
    anonymous_delete_response = client.delete(f"/authorized-students/{student_id}")

    assert anonymous_module_response.status_code == status.HTTP_401_UNAUTHORIZED
    assert anonymous_student_response.status_code == status.HTTP_401_UNAUTHORIZED
    assert anonymous_add_response.status_code == status.HTTP_401_UNAUTHORIZED
    assert anonymous_update_response.status_code == status.HTTP_401_UNAUTHORIZED
    assert anonymous_delete_response.status_code == status.HTTP_401_UNAUTHORIZED

    invalid_token_response = client.get(
        f"/authorized-students/module/{module.module_id}",
        headers={"Authorization": "Bearer not-a-valid-token"},
    )

    assert invalid_token_response.status_code == status.HTTP_401_UNAUTHORIZED


def test_owner_can_retrieve_authorized_student_by_id(client, db_session):
    """Module managers can retrieve a single authorized student by id."""
    owner_id, owner_auth = _register_user(client, "student-retrieval-owner@example.com")
    created = _create_channel(client, owner_auth, owner_id, "Student Retrieval Channel")
    module = _create_module(db_session, created["channel_id"], owner_id)

    add_response = _add_student(client, owner_auth, module.module_id)
    assert add_response.status_code == status.HTTP_200_OK
    student_id = add_response.json()["id"]

    get_response = client.get(f"/authorized-students/{student_id}", headers=owner_auth)

    assert get_response.status_code == status.HTTP_200_OK
    body = get_response.json()
    assert body["id"] == student_id
    assert body["channel_module_id"] == module.module_id
    assert body["student_name"] == "Authorized Student"
    assert body["student_email"] == "authorized-student@example.com"
    assert body["status"] == "active"


def test_unauthorized_user_cannot_retrieve_students_by_module(client, db_session):
    """Authenticated users outside the module scope cannot list students."""
    owner_id, owner_auth = _register_user(client, "module-list-owner@example.com")
    _attacker_id, attacker_auth = _register_user(client, "module-list-attacker@example.com")
    created = _create_channel(client, owner_auth, owner_id, "Module List Channel")
    module = _create_module(db_session, created["channel_id"], owner_id)

    add_response = _add_student(client, owner_auth, module.module_id)
    assert add_response.status_code == status.HTTP_200_OK
    student_id = add_response.json()["id"]

    attacker_module_response = client.get(
        f"/authorized-students/module/{module.module_id}",
        headers=attacker_auth,
    )
    attacker_student_response = client.get(
        f"/authorized-students/{student_id}",
        headers=attacker_auth,
    )

    assert attacker_module_response.status_code == status.HTTP_403_FORBIDDEN
    assert attacker_student_response.status_code == status.HTTP_403_FORBIDDEN


def test_student_records_outside_manager_scope_are_not_retrievable(client, db_session):
    """A module owner cannot retrieve students that belong to another module."""
    owner_a_id, owner_a_auth = _register_user(client, "scope-owner-a@example.com")
    owner_b_id, owner_b_auth = _register_user(client, "scope-owner-b@example.com")
    created_a = _create_channel(client, owner_a_auth, owner_a_id, "Scope Channel A")
    module_a = _create_module(db_session, created_a["channel_id"], owner_a_id)

    add_response = _add_student(client, owner_a_auth, module_a.module_id)
    assert add_response.status_code == status.HTTP_200_OK
    student_id = add_response.json()["id"]

    owner_b_student_response = client.get(
        f"/authorized-students/{student_id}",
        headers=owner_b_auth,
    )
    owner_b_module_response = client.get(
        f"/authorized-students/module/{module_a.module_id}",
        headers=owner_b_auth,
    )

    assert owner_b_student_response.status_code == status.HTTP_403_FORBIDDEN
    assert owner_b_module_response.status_code == status.HTTP_403_FORBIDDEN


def test_invalid_student_module_and_channel_identifiers_are_rejected(client, db_session):
    """Malformed identifiers and email addresses are rejected before lookup."""
    owner_id, owner_auth = _register_user(client, "invalid-id-owner@example.com")
    created = _create_channel(client, owner_auth, owner_id, "Invalid Id Channel")
    module = _create_module(db_session, created["channel_id"], owner_id)

    invalid_student_response = client.get(
        "/authorized-students/not-an-integer",
        headers=owner_auth,
    )
    invalid_module_response = client.get(
        "/authorized-students/module/not-an-integer",
        headers=owner_auth,
    )
    invalid_channel_response = client.get("/channels/not-an-integer")
    invalid_add_response = client.post(
        "/authorized-students/",
        json={
            "channel_module_id": module.module_id,
            "student_name": "Invalid Email Student",
            "student_email": "not-a-valid-email",
            "status": "active",
            "remark": None,
        },
        headers=owner_auth,
    )

    assert invalid_student_response.status_code == 422
    assert invalid_module_response.status_code == 422
    assert invalid_channel_response.status_code == 422
    assert invalid_add_response.status_code == 422


def test_authorized_student_impersonation_attempts_are_rejected(client, db_session):
    """The acting user can never target another user through query parameters."""
    owner_id, owner_auth = _register_user(client, "impersonation-owner@example.com")
    attacker_id, _attacker_auth = _register_user(client, "impersonation-attacker@example.com")
    created = _create_channel(client, owner_auth, owner_id, "Impersonation Channel")
    module = _create_module(db_session, created["channel_id"], owner_id)

    add_response = _add_student(client, owner_auth, module.module_id)
    assert add_response.status_code == status.HTTP_200_OK
    student_id = add_response.json()["id"]

    impersonated_module_response = client.get(
        f"/authorized-students/module/{module.module_id}",
        params={"user_id": attacker_id},
        headers=owner_auth,
    )
    impersonated_student_response = client.get(
        f"/authorized-students/{student_id}",
        params={"user_id": attacker_id},
        headers=owner_auth,
    )
    impersonated_add_response = client.post(
        "/authorized-students/",
        json={
            "channel_module_id": module.module_id,
            "student_name": "Impersonated Student",
            "student_email": "impersonated-student@example.com",
            "status": "active",
            "remark": None,
        },
        params={"user_id": attacker_id},
        headers=owner_auth,
    )

    assert impersonated_module_response.status_code == status.HTTP_403_FORBIDDEN
    assert impersonated_student_response.status_code == status.HTTP_403_FORBIDDEN
    assert impersonated_add_response.status_code == status.HTTP_403_FORBIDDEN


def test_module_co_host_can_retrieve_module_students(client, db_session):
    """Module co-hosts may retrieve the students they manage."""
    owner_id, owner_auth = _register_user(client, "cohost-retrieval-owner@example.com")
    cohost_id, cohost_auth = _register_user(client, "cohost-retrieval@example.com")
    created = _create_channel(client, owner_auth, owner_id, "Co-host Retrieval Channel")
    module = ChannelModule(
        channel_id=created["channel_id"],
        user_id=owner_id,
        name="Co-host Retrieval Module",
        description="Module used for co-host student retrieval",
        co_host_email="cohost-retrieval@example.com",
        visibility=VisibilityEnum.public,
    )
    db_session.add(module)
    db_session.commit()
    db_session.refresh(module)

    add_response = _add_student(client, owner_auth, module.module_id)
    assert add_response.status_code == status.HTTP_200_OK
    student_id = add_response.json()["id"]

    cohost_module_response = client.get(
        f"/authorized-students/module/{module.module_id}",
        headers=cohost_auth,
    )
    cohost_student_response = client.get(
        f"/authorized-students/{student_id}",
        headers=cohost_auth,
    )

    assert cohost_module_response.status_code == status.HTTP_200_OK
    assert len(cohost_module_response.json()) == 1
    assert cohost_student_response.status_code == status.HTTP_200_OK


def test_student_endpoint_error_details_are_stable_for_missing_records(client, db_session):
    """Missing module and student records return stable error contracts."""
    owner_id, owner_auth = _register_user(client, "error-detail-owner@example.com")
    created = _create_channel(client, owner_auth, owner_id, "Error Detail Channel")
    module = _create_module(db_session, created["channel_id"], owner_id)

    missing_module_response = client.get(
        "/authorized-students/module/999999",
        headers=owner_auth,
    )
    missing_student_response = client.get(
        "/authorized-students/999999",
        headers=owner_auth,
    )

    assert missing_module_response.status_code == 404
    assert missing_module_response.json()["detail"] == "Channel module not found"
    assert missing_student_response.status_code == 404
    assert missing_student_response.json()["detail"] == "Student not found"


def test_student_module_access_error_response_is_consistent(client, db_session):
    """Unauthorized module access returns a stable error contract."""
    owner_id, owner_auth = _register_user(client, "error-access-owner@example.com")
    _attacker_id, attacker_auth = _register_user(client, "error-access-attacker@example.com")
    created = _create_channel(client, owner_auth, owner_id, "Error Access Channel")
    module = _create_module(db_session, created["channel_id"], owner_id)

    add_response = _add_student(client, owner_auth, module.module_id)
    assert add_response.status_code == status.HTTP_200_OK
    student_id = add_response.json()["id"]

    attacker_response = client.get(
        f"/authorized-students/{student_id}",
        headers=attacker_auth,
    )

    assert attacker_response.status_code == status.HTTP_403_FORBIDDEN
    assert attacker_response.json()["detail"] == "Not authorized to manage students for this channel"


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
