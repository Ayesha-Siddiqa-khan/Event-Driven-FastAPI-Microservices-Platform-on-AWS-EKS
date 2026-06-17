from typing import Any

from app.clients.http_client import UpstreamResponse, check_upstream_ready, request_json
from app.config import settings

UPSTREAM_SERVICE = "payment-service"


class PaymentServiceClient:
    """Client for payment-service gateway operations."""

    async def create_payment(self, order_id: int, payload: dict[str, Any]) -> UpstreamResponse:
        return await request_json(
            UPSTREAM_SERVICE,
            "POST",
            settings.payment_service_url,
            f"/payments/{order_id}",
            payload,
        )

    async def ready(self) -> bool:
        return await check_upstream_ready(UPSTREAM_SERVICE, settings.payment_service_url)


def get_payment_client() -> PaymentServiceClient:
    return PaymentServiceClient()
