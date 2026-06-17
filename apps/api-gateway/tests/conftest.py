from collections.abc import Generator
from pathlib import Path
import sys
from typing import Any

import pytest
from fastapi.testclient import TestClient

SERVICE_ROOT = Path(__file__).resolve().parents[1]
if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))

from app.clients.auth_client import get_auth_client  # noqa: E402
from app.clients.http_client import UpstreamResponse  # noqa: E402
from app.clients.order_client import get_order_client  # noqa: E402
from app.clients.payment_client import get_payment_client  # noqa: E402
from app.main import app  # noqa: E402


class FakeAuthClient:
    def __init__(self) -> None:
        self.ready_result = True
        self.register_payload: dict[str, Any] | None = None
        self.login_payload: dict[str, Any] | None = None

    async def ready(self) -> bool:
        return self.ready_result

    async def register(self, payload: dict[str, Any]) -> UpstreamResponse:
        self.register_payload = payload
        return UpstreamResponse(201, {"id": 1, "email": payload["email"], "created_at": "2026-01-01T00:00:00Z"})

    async def login(self, payload: dict[str, Any]) -> UpstreamResponse:
        self.login_payload = payload
        return UpstreamResponse(200, {"token": "test-token", "user_id": 1})


class FakeOrderClient:
    def __init__(self) -> None:
        self.ready_result = True
        self.create_payload: dict[str, Any] | None = None
        self.lookup_order_id: int | None = None

    async def ready(self) -> bool:
        return self.ready_result

    async def create_order(self, payload: dict[str, Any]) -> UpstreamResponse:
        self.create_payload = payload
        return UpstreamResponse(201, {"id": 10, "user_id": payload["user_id"], "amount": payload["amount"], "status": "created"})

    async def get_order(self, order_id: int) -> UpstreamResponse:
        self.lookup_order_id = order_id
        return UpstreamResponse(200, {"id": order_id, "user_id": 1, "amount": "25.50", "status": "created"})


class FakePaymentClient:
    def __init__(self) -> None:
        self.ready_result = True
        self.payment_order_id: int | None = None
        self.payment_payload: dict[str, Any] | None = None

    async def ready(self) -> bool:
        return self.ready_result

    async def create_payment(self, order_id: int, payload: dict[str, Any]) -> UpstreamResponse:
        self.payment_order_id = order_id
        self.payment_payload = payload
        return UpstreamResponse(201, {"id": 99, "order_id": order_id, "amount": payload["amount"], "status": "success"})


@pytest.fixture()
def fake_auth_client() -> FakeAuthClient:
    return FakeAuthClient()


@pytest.fixture()
def fake_order_client() -> FakeOrderClient:
    return FakeOrderClient()


@pytest.fixture()
def fake_payment_client() -> FakePaymentClient:
    return FakePaymentClient()


@pytest.fixture()
def client(
    fake_auth_client: FakeAuthClient,
    fake_order_client: FakeOrderClient,
    fake_payment_client: FakePaymentClient,
) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_auth_client] = lambda: fake_auth_client
    app.dependency_overrides[get_order_client] = lambda: fake_order_client
    app.dependency_overrides[get_payment_client] = lambda: fake_payment_client

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
