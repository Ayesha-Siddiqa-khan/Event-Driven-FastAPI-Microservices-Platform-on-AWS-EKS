from typing import Any

from app.clients.http_client import UpstreamResponse, check_upstream_ready, request_json
from app.config import settings

UPSTREAM_SERVICE = "auth-service"


class AuthServiceClient:
    """Client for auth-service public gateway operations."""

    async def register(self, payload: dict[str, Any]) -> UpstreamResponse:
        return await request_json(UPSTREAM_SERVICE, "POST", settings.auth_service_url, "/register", payload)

    async def login(self, payload: dict[str, Any]) -> UpstreamResponse:
        return await request_json(UPSTREAM_SERVICE, "POST", settings.auth_service_url, "/login", payload)

    async def ready(self) -> bool:
        return await check_upstream_ready(UPSTREAM_SERVICE, settings.auth_service_url)


def get_auth_client() -> AuthServiceClient:
    return AuthServiceClient()
