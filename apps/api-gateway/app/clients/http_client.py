from dataclasses import dataclass
import logging
from typing import Any

import httpx

from app.config import settings
from app.metrics import record_upstream_failure, record_upstream_request

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class UpstreamResponse:
    status_code: int
    body: Any


class UpstreamTimeoutError(Exception):
    def __init__(self, upstream_service: str, path: str) -> None:
        self.upstream_service = upstream_service
        self.path = path
        super().__init__(f"{upstream_service} timed out")


class UpstreamUnavailableError(Exception):
    def __init__(self, upstream_service: str, path: str, message: str) -> None:
        self.upstream_service = upstream_service
        self.path = path
        self.message = message
        super().__init__(message)


def _join_url(base_url: str, path: str) -> str:
    return f"{base_url.rstrip('/')}/{path.lstrip('/')}"


def _response_body(response: httpx.Response) -> Any:
    try:
        return response.json()
    except ValueError:
        if response.text:
            return {"detail": response.text}
        return {"status": "ok"}


async def request_json(
    upstream_service: str,
    method: str,
    base_url: str,
    path: str,
    payload: dict[str, Any] | None = None,
) -> UpstreamResponse:
    """Forward a JSON request to an upstream service and normalize failures."""
    url = _join_url(base_url, path)

    try:
        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
            response = await client.request(method=method, url=url, json=payload)
    except httpx.TimeoutException as exc:
        record_upstream_failure(upstream_service, "timeout")
        logger.warning(
            "upstream_timeout",
            extra={
                "event": "upstream_timeout",
                "upstream_service": upstream_service,
                "path": path,
                "error": str(exc),
            },
        )
        raise UpstreamTimeoutError(upstream_service, path) from exc
    except httpx.RequestError as exc:
        record_upstream_failure(upstream_service, "unavailable")
        logger.warning(
            "upstream_unavailable",
            extra={
                "event": "upstream_unavailable",
                "upstream_service": upstream_service,
                "path": path,
                "error": str(exc),
            },
        )
        raise UpstreamUnavailableError(upstream_service, path, str(exc)) from exc

    record_upstream_request(upstream_service, method, path, response.status_code)
    if response.status_code >= 400:
        record_upstream_failure(upstream_service, "status_code")
        logger.info(
            "upstream_error_response",
            extra={
                "event": "upstream_error_response",
                "upstream_service": upstream_service,
                "path": path,
                "status_code": response.status_code,
            },
        )

    return UpstreamResponse(status_code=response.status_code, body=_response_body(response))


async def check_upstream_ready(upstream_service: str, base_url: str) -> bool:
    """Check an upstream service readiness endpoint, falling back to health."""
    for path in ("/ready", "/health"):
        try:
            response = await request_json(upstream_service, "GET", base_url, path)
        except (UpstreamTimeoutError, UpstreamUnavailableError):
            continue
        if response.status_code == 200:
            return True
    return False
