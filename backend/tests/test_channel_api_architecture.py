"""Architecture, legacy-router, and OpenAPI compatibility tests for channels."""

import inspect

from fastapi import status


def test_legacy_route_wrappers_resolve_to_canonical_routers():
    from app.routes import authorized_students as canonical_authorized
    from app.routes import channel as canonical_channel
    from app.routes import channel_analytic as canonical_analytics
    from routes import authorized_students as legacy_authorized
    from routes import channel as legacy_channel
    from routes import channel_analytic as legacy_analytics

    assert legacy_channel.router is canonical_channel.router
    assert legacy_authorized.router is canonical_authorized.router
    assert legacy_analytics.router is canonical_analytics.router


def test_openapi_schema_includes_channel_endpoints(client):
    response = client.get("/openapi.json")

    assert response.status_code == status.HTTP_200_OK
    paths = set(response.json()["paths"])
    expected_paths = {
        "/channels/",
        "/channels/{channel_id}",
        "/channels/{channel_id}/authorize",
        "/channel-analytics/{user_id}",
        "/authorized-students/",
        "/authorized-students/module/{module_id}",
        "/authorized-students/{student_id}",
    }
    assert expected_paths.issubset(paths)


def test_openapi_marks_protected_channel_endpoints_as_bearer_protected(client):
    paths = client.get("/openapi.json").json()["paths"]

    protected = {
        ("post", "/channels/"),
        ("put", "/channels/{channel_id}"),
        ("delete", "/channels/{channel_id}"),
        ("get", "/channels/{channel_id}/authorize"),
        ("get", "/channel-analytics/{user_id}"),
        ("post", "/authorized-students/"),
        ("get", "/authorized-students/module/{module_id}"),
        ("get", "/authorized-students/{student_id}"),
        ("put", "/authorized-students/{student_id}"),
        ("delete", "/authorized-students/{student_id}"),
    }

    for method, path in protected:
        operation = paths[path][method]
        security = operation.get("security") or []
        assert any(
            "OAuth2PasswordBearer" in requirement for requirement in security
        ), f"{method.upper()} {path} must require bearer authentication"

    public_reads = {
        ("get", "/channels/"),
        ("get", "/channels/public"),
        ("get", "/channels/user/{user_id}"),
        ("get", "/channels/{channel_id}"),
    }

    for method, path in public_reads:
        assert not paths[path][method].get("security"), (
            f"{method.upper()} {path} must remain a public read"
        )


def test_channel_route_delegates_to_controller_and_service_only():
    from app import repositories as app_repositories
    from app import routes as app_routes
    from app import services as app_services
    from app.controllers import channel_controller

    route_source = inspect.getsource(app_routes.channel)
    assert "from app.controllers import channel_controller" in route_source
    assert "app.services.channel_service" in route_source
    assert "app.repositories.channel_repository" not in route_source

    controller_source = inspect.getsource(channel_controller)
    assert "app.repositories.channel_repository" not in controller_source
    assert "from app.services import channel_service" in controller_source

    service_source = inspect.getsource(app_services.channel_service)
    assert "from app.repositories import channel_repository" in service_source
    assert "from app.controllers import channel_controller" not in service_source
    assert "app.routes.channel" not in service_source


def test_channel_repository_contains_database_operations():
    from app import repositories as app_repositories

    repository_source = inspect.getsource(app_repositories.channel_repository)
    assert "db.query" in repository_source


def test_channel_layers_import_without_cycle():
    from app.controllers import channel_controller
    from app.repositories import channel_repository
    from app.routes import channel as channel_route
    from app.services import channel_service

    assert channel_controller is not None
    assert channel_repository is not None
    assert channel_route is not None
    assert channel_service is not None
