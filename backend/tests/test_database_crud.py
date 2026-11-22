"""Database-backed tests using the centralized session dependency and fixtures."""

from app.models.user import User


def test_signup_endpoint_persists_user(client, db_session):
    """The API must receive its database session from the centralized dependency."""
    response = client.post(
        "/auth/signup",
        json={"email": "student@example.com", "password": "strong-password"},
    )

    assert response.status_code == 201
    assert response.json()["user_id"] is not None

    user = db_session.query(User).filter(User.email == "student@example.com").one()
    assert user.email == "student@example.com"


def test_login_endpoint_reads_user_from_database(client, db_session):
    client.post(
        "/auth/signup",
        json={"email": "student@example.com", "password": "strong-password"},
    )

    response = client.post(
        "/auth/login",
        json={"email": "student@example.com", "password": "strong-password"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
