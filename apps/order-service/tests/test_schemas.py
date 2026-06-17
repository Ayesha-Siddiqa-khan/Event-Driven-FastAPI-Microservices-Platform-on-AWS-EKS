from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas import OrderCreate


def test_order_create_schema_accepts_valid_payload() -> None:
    payload = OrderCreate(user_id=5, amount=Decimal("10.25"))

    assert payload.user_id == 5
    assert payload.amount == Decimal("10.25")


@pytest.mark.parametrize(
    "payload",
    [
        {"user_id": 0, "amount": "10.00"},
        {"user_id": 1, "amount": "0.00"},
        {"user_id": 1, "amount": "-1.00"},
        {"user_id": 1, "amount": "10.999"},
    ],
)
def test_order_create_schema_rejects_invalid_payload(payload: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        OrderCreate(**payload)
