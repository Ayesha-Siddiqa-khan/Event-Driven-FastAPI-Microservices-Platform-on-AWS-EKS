import json

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Payment


def test_create_payment_records_success_and_publishes_sqs_message(
    client: TestClient,
    db_session: Session,
    fake_sqs,
) -> None:
    response = client.post("/payments/1", json={"amount": "42.50"})

    assert response.status_code == 201
    body = response.json()
    assert body["order_id"] == 1
    assert body["status"] == "success"

    payment = db_session.get(Payment, body["id"])
    assert payment is not None
    assert payment.order_id == 1
    assert payment.status == "success"

    assert len(fake_sqs.messages) == 1
    message = fake_sqs.messages[0]
    assert message["QueueUrl"] == "http://sqs.local/queue/notification-events"
    assert json.loads(message["MessageBody"]) == {
        "event_type": "payment_completed",
        "order_id": "1",
        "payment_id": str(body["id"]),
        "status": "success",
    }


def test_create_payment_can_fail_in_random_mode(client: TestClient, monkeypatch) -> None:
    monkeypatch.setattr(settings, "payment_success_mode", "random")
    monkeypatch.setattr("app.routes.random.choice", lambda values: values[1])

    response = client.post("/payments/1", json={"amount": "42.50"})

    assert response.status_code == 201
    assert response.json()["status"] == "failed"


def test_get_payment_returns_payment_information(client: TestClient) -> None:
    created = client.post("/payments/1", json={"amount": "42.50"}).json()

    response = client.get(f"/payments/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
    assert response.json()["order_id"] == 1


def test_get_payment_returns_clear_404_for_missing_payment(client: TestClient) -> None:
    response = client.get("/payments/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"
