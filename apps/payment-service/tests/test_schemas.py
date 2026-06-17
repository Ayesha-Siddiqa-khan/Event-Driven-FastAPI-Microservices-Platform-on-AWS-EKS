from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas import PaymentCreate


def test_payment_create_schema_accepts_valid_payload() -> None:
    payload = PaymentCreate(amount=Decimal("10.25"))

    assert payload.amount == Decimal("10.25")


@pytest.mark.parametrize(
    "payload",
    [
        {"amount": "0.00"},
        {"amount": "-1.00"},
        {"amount": "10.999"},
    ],
)
def test_payment_create_schema_rejects_invalid_payload(payload: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        PaymentCreate(**payload)
