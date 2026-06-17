from typing import Annotated

from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse

from app.clients.auth_client import AuthServiceClient, get_auth_client
from app.clients.http_client import UpstreamResponse, UpstreamTimeoutError, UpstreamUnavailableError
from app.clients.order_client import OrderServiceClient, get_order_client
from app.clients.payment_client import PaymentServiceClient, get_payment_client
from app.schemas import LoginRequest, OrderCreateRequest, PaymentCreateRequest, RegisterRequest

router = APIRouter(prefix="/api")


def gateway_response(response: UpstreamResponse) -> JSONResponse:
    """Return the upstream response body with its original status code."""
    return JSONResponse(status_code=response.status_code, content=response.body)


def upstream_timeout_response(exc: UpstreamTimeoutError) -> JSONResponse:
    return JSONResponse(
        status_code=504,
        content={
            "detail": "Upstream service timed out",
            "upstream_service": exc.upstream_service,
        },
    )


def upstream_unavailable_response(exc: UpstreamUnavailableError) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={
            "detail": "Upstream service unavailable",
            "upstream_service": exc.upstream_service,
        },
    )


async def handle_upstream(call) -> JSONResponse:
    try:
        response = await call()
    except UpstreamTimeoutError as exc:
        return upstream_timeout_response(exc)
    except UpstreamUnavailableError as exc:
        return upstream_unavailable_response(exc)
    return gateway_response(response)


@router.post("/register")
async def register(
    payload: RegisterRequest,
    auth_client: Annotated[AuthServiceClient, Depends(get_auth_client)],
) -> JSONResponse:
    """Forward registration requests to auth-service."""
    return await handle_upstream(lambda: auth_client.register(payload.model_dump(mode="json")))


@router.post("/login")
async def login(
    payload: LoginRequest,
    auth_client: Annotated[AuthServiceClient, Depends(get_auth_client)],
) -> JSONResponse:
    """Forward login requests to auth-service."""
    return await handle_upstream(lambda: auth_client.login(payload.model_dump(mode="json")))


@router.post("/orders")
async def create_order(
    payload: OrderCreateRequest,
    order_client: Annotated[OrderServiceClient, Depends(get_order_client)],
) -> JSONResponse:
    """Forward order creation requests to order-service."""
    return await handle_upstream(lambda: order_client.create_order(payload.model_dump(mode="json")))


@router.get("/orders/{order_id}")
async def get_order(
    order_id: Annotated[int, Path(gt=0)],
    order_client: Annotated[OrderServiceClient, Depends(get_order_client)],
) -> JSONResponse:
    """Forward order lookup requests to order-service."""
    return await handle_upstream(lambda: order_client.get_order(order_id))


@router.post("/payments/{order_id}")
async def create_payment(
    order_id: Annotated[int, Path(gt=0)],
    payload: PaymentCreateRequest,
    payment_client: Annotated[PaymentServiceClient, Depends(get_payment_client)],
) -> JSONResponse:
    """Forward payment creation requests to payment-service."""
    return await handle_upstream(lambda: payment_client.create_payment(order_id, payload.model_dump(mode="json")))
