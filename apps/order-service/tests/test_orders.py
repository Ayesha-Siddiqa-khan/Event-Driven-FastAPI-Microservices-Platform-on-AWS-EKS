import json

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Order


def test_create_order_caches_order_and_publishes_sqs_message(
    client: TestClient,
    db_session: Session,
    fake_redis,
    fake_sqs,
) -> None:
    response = client.post("/orders", json={"user_id": 5, "amount": "100.00"})

    assert response.status_code == 201
    body = response.json()
    assert body["user_id"] == 5
    assert body["status"] == "created"

    order = db_session.get(Order, body["id"])
    assert order is not None

    cached = fake_redis.get_json(f"order:{body['id']}")
    assert cached["id"] == body["id"]
    assert cached["user_id"] == 5

    assert len(fake_sqs.messages) == 1
    message = fake_sqs.messages[0]
    assert message["QueueUrl"] == "http://sqs.local/queue/order-events"
    assert json.loads(message["MessageBody"]) == {
        "event_type": "order_created",
        "order_id": str(body["id"]),
        "user_id": "5",
        "amount": 100,
    }


def test_get_order_reads_from_cache_first(client: TestClient, fake_redis) -> None:
    created = client.post("/orders", json={"user_id": 5, "amount": "12.34"}).json()

    response = client.get(f"/orders/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
    assert fake_redis.get_json(f"order:{created['id']}")["user_id"] == 5


def test_list_orders_returns_orders(client: TestClient) -> None:
    first = client.post("/orders", json={"user_id": 5, "amount": "10.00"}).json()
    second = client.post("/orders", json={"user_id": 6, "amount": "20.00"}).json()

    response = client.get("/orders")

    assert response.status_code == 200
    assert [order["id"] for order in response.json()] == [second["id"], first["id"]]
