from typing import Any

from app.clients.http_client import UpstreamResponse, check_upstream_ready, request_json
from app.config import settings

UPSTREAM_SERVICE = "order-service"


class OrderServiceClient:
    """Client for order-service gateway operations."""

    async def create_order(self, payload: dict[str, Any]) -> UpstreamResponse:
        return await request_json(UPSTREAM_SERVICE, "POST", settings.order_service_url, "/orders", payload)

    async def get_order(self, order_id: int) -> UpstreamResponse:
        return await request_json(UPSTREAM_SERVICE, "GET", settings.order_service_url, f"/orders/{order_id}")

    async def ready(self) -> bool:
        return await check_upstream_ready(UPSTREAM_SERVICE, settings.order_service_url)


def get_order_client() -> OrderServiceClient:
    return OrderServiceClient()
