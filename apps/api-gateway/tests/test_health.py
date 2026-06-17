from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "api-gateway"


def test_ready_returns_200_when_internal_services_are_ready(client: TestClient) -> None:
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "checks": {
            "auth-service": "ok",
            "order-service": "ok",
            "payment-service": "ok",
        },
    }


def test_ready_returns_503_when_internal_service_is_not_ready(client: TestClient, fake_order_client) -> None:
    fake_order_client.ready_result = False

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"
    assert response.json()["checks"]["order-service"] == "failed"


def test_metrics_endpoint(client: TestClient) -> None:
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "api_gateway_http_requests_total" in response.text
