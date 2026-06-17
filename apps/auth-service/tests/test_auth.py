from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import User
from app.security import verify_password


def test_register_creates_user_with_hashed_password(client: TestClient, db_session: Session) -> None:
    response = client.post(
        "/register",
        json={"email": "Person@Example.com", "password": "correct-password"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "person@example.com"
    assert "password_hash" not in body

    user = db_session.query(User).filter(User.email == "person@example.com").one()
    assert user.password_hash != "correct-password"
    assert verify_password("correct-password", user.password_hash)


def test_register_rejects_duplicate_email(client: TestClient) -> None:
    payload = {"email": "person@example.com", "password": "correct-password"}

    assert client.post("/register", json=payload).status_code == 201
    response = client.post("/register", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


def test_login_stores_fake_session_token(client: TestClient, fake_redis) -> None:
    register_response = client.post(
        "/register",
        json={"email": "person@example.com", "password": "correct-password"},
    )
    user_id = register_response.json()["id"]

    response = client.post(
        "/login",
        json={"email": "person@example.com", "password": "correct-password"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == user_id
    assert fake_redis.get(f"session:{body['token']}") == str(user_id)


def test_login_rejects_invalid_credentials(client: TestClient) -> None:
    client.post(
        "/register",
        json={"email": "person@example.com", "password": "correct-password"},
    )

    response = client.post(
        "/login",
        json={"email": "person@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_get_user_returns_public_user_information(client: TestClient) -> None:
    register_response = client.post(
        "/register",
        json={"email": "person@example.com", "password": "correct-password"},
    )
    user_id = register_response.json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["email"] == "person@example.com"


def test_get_user_returns_404_for_missing_user(client: TestClient) -> None:
    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
