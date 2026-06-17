from fastapi.testclient import TestClient

from app import main as main_module


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready_returns_200_when_dependencies_are_available(client: TestClient, monkeypatch) -> None:
    monkeypatch.setattr(main_module, "check_database", lambda: True)
    monkeypatch.setattr(main_module, "check_redis", lambda: True)

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "checks": {"postgres": "ok", "redis": "ok"},
    }


def test_ready_returns_503_when_dependency_is_unavailable(client: TestClient, monkeypatch) -> None:
    monkeypatch.setattr(main_module, "check_database", lambda: True)
    monkeypatch.setattr(main_module, "check_redis", lambda: False)

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json() == {
        "status": "not_ready",
        "checks": {"postgres": "ok", "redis": "failed"},
    }


def test_metrics_endpoint(client: TestClient) -> None:
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "user_registrations_total" in response.text
