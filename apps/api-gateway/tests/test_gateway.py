from fastapi.testclient import TestClient

from app.clients.http_client import UpstreamTimeoutError, UpstreamUnavailableError


def test_register_forwarding(client: TestClient, fake_auth_client) -> None:
    response = client.post("/api/register", json={"email": "person@example.com", "password": "secret123"})

    assert response.status_code == 201
    assert response.json()["email"] == "person@example.com"
    assert fake_auth_client.register_payload == {"email": "person@example.com", "password": "secret123"}


def test_login_forwarding(client: TestClient, fake_auth_client) -> None:
    response = client.post("/api/login", json={"email": "person@example.com", "password": "secret123"})

    assert response.status_code == 200
    assert response.json() == {"token": "test-token", "user_id": 1}
    assert fake_auth_client.login_payload == {"email": "person@example.com", "password": "secret123"}


def test_create_order_forwarding(client: TestClient, fake_order_client) -> None:
    response = client.post("/api/orders", json={"user_id": 1, "amount": "25.50"})

    assert response.status_code == 201
    assert response.json()["status"] == "created"
    assert fake_order_client.create_payload == {"user_id": 1, "amount": "25.50"}


def test_get_order_forwarding(client: TestClient, fake_order_client) -> None:
    response = client.get("/api/orders/10")

    assert response.status_code == 200
    assert response.json()["id"] == 10
    assert fake_order_client.lookup_order_id == 10


def test_create_payment_forwarding(client: TestClient, fake_payment_client) -> None:
    response = client.post("/api/payments/10", json={"amount": "25.50"})

    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert fake_payment_client.payment_order_id == 10
    assert fake_payment_client.payment_payload == {"amount": "25.50"}


def test_upstream_timeout_returns_504(client: TestClient, fake_auth_client, monkeypatch) -> None:
    async def timeout(payload):
        raise UpstreamTimeoutError("auth-service", "/register")

    monkeypatch.setattr(fake_auth_client, "register", timeout)

    response = client.post("/api/register", json={"email": "person@example.com", "password": "secret123"})

    assert response.status_code == 504
    assert response.json() == {
        "detail": "Upstream service timed out",
        "upstream_service": "auth-service",
    }


def test_upstream_unavailable_returns_503(client: TestClient, fake_order_client, monkeypatch) -> None:
    async def unavailable(payload):
        raise UpstreamUnavailableError("order-service", "/orders", "connection failed")

    monkeypatch.setattr(fake_order_client, "create_order", unavailable)

    response = client.post("/api/orders", json={"user_id": 1, "amount": "25.50"})

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Upstream service unavailable",
        "upstream_service": "order-service",
    }
