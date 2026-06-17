import json

from app.sqs_client import build_payment_completed_message, serialize_payment_completed_message


def test_build_payment_completed_message_uses_required_payload_shape() -> None:
    assert build_payment_completed_message(order_id=1, payment_id=10, status="success") == {
        "event_type": "payment_completed",
        "order_id": "1",
        "payment_id": "10",
        "status": "success",
    }


def test_serialize_payment_completed_message_returns_json() -> None:
    message = serialize_payment_completed_message(order_id=1, payment_id=10, status="success")

    assert json.loads(message) == {
        "event_type": "payment_completed",
        "order_id": "1",
        "payment_id": "10",
        "status": "success",
    }
