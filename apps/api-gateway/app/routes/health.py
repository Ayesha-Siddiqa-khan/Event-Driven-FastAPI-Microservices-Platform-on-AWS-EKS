from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.clients.auth_client import AuthServiceClient, get_auth_client
from app.clients.order_client import OrderServiceClient, get_order_client
from app.clients.payment_client import PaymentServiceClient, get_payment_client
from app.config import settings
from app.metrics import record_readiness, render_metrics

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """Return liveness status for the gateway process."""
    return {
        "status": "ok",
        "service": settings.service_name,
        "environment": settings.environment,
    }


@router.get("/ready")
async def ready(
    response: Response,
    auth_client: Annotated[AuthServiceClient, Depends(get_auth_client)],
    order_client: Annotated[OrderServiceClient, Depends(get_order_client)],
    payment_client: Annotated[PaymentServiceClient, Depends(get_payment_client)],
) -> dict[str, object]:
    """Return readiness status for internal service dependencies only."""
    raw_checks = {
        "auth-service": await auth_client.ready(),
        "order-service": await order_client.ready(),
        "payment-service": await payment_client.ready(),
    }
    for upstream_service, healthy in raw_checks.items():
        record_readiness(upstream_service, healthy)

    checks = {upstream_service: "ok" if healthy else "failed" for upstream_service, healthy in raw_checks.items()}
    ready_status = all(raw_checks.values())
    if not ready_status:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "ready" if ready_status else "not_ready", "checks": checks}


@router.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    """Return Prometheus metrics."""
    body, media_type = render_metrics()
    return Response(content=body, media_type=media_type)
