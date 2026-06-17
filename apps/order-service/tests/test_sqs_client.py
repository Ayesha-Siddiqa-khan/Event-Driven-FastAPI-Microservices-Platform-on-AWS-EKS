import json
from decimal import Decimal

from app.sqs_client import build_order_created_message, serialize_order_created_message


def test_build_order_created_message_uses_required_payload_shape() -> None:
    assert build_order_created_message(order_id=1, user_id=5, amount=Decimal("100.00")) == {
        "event_type": "order_created",
        "order_id": "1",
        "user_id": "5",
        "amount": 100,
    }


def test_serialize_order_created_message_returns_json() -> None:
    message = serialize_order_created_message(order_id=1, user_id=5, amount=Decimal("12.34"))

    assert json.loads(message) == {
        "event_type": "order_created",
        "order_id": "1",
        "user_id": "5",
        "amount": 12.34,
    }
