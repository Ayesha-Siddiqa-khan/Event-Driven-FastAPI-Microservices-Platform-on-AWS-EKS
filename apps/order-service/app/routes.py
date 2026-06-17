import logging
from decimal import Decimal
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.metrics import ORDERS_CREATED, ORDER_CACHE_HITS, ORDER_CACHE_MISSES
from app.models import Order, OrderStatus
from app.redis_client import RedisError, cache_order, get_cached_order, get_redis
from app.schemas import OrderCreate, OrderResponse
from app.sqs_client import SqsError, get_sqs_client, publish_order_created

logger = logging.getLogger(__name__)
router = APIRouter()

DbSession = Annotated[Session, Depends(get_db)]
RedisClient = Annotated[Any, Depends(get_redis)]
SqsClient = Annotated[Any, Depends(get_sqs_client)]


def order_to_dict(order: Order) -> dict[str, Any]:
    """Convert an Order model to a cache-safe response payload."""
    return {
        "id": order.id,
        "user_id": order.user_id,
        "amount": str(order.amount),
        "status": order.status,
        "created_at": order.created_at.isoformat() if order.created_at else None,
    }


@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, db: DbSession, redis_client: RedisClient, sqs_client: SqsClient) -> Order:
    """Create an order, cache it, and publish an order_created event."""
    order = Order(user_id=payload.user_id, amount=payload.amount, status=OrderStatus.CREATED.value)

    try:
        db.add(order)
        db.commit()
        db.refresh(order)
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("order_create_database_error", extra={"event": "order_create_database_error"})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create order",
        ) from exc

    try:
        cache_order(redis_client, order.id, order_to_dict(order), settings.order_cache_ttl_seconds)
    except (RedisError, ValueError, TypeError) as exc:
        logger.exception(
            "order_cache_write_failed",
            extra={"event": "order_cache_write_failed", "order_id": order.id, "error": str(exc)},
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Order cache unavailable",
        ) from exc

    try:
        publish_order_created(sqs_client, order.id, order.user_id, Decimal(order.amount))
    except (RuntimeError, SqsError) as exc:
        logger.exception(
            "order_event_publish_failed",
            extra={"event": "order_event_publish_failed", "order_id": order.id, "error": str(exc)},
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Order event publishing unavailable",
        ) from exc

    ORDERS_CREATED.inc()
    logger.info("order_created", extra={"event": "order_created", "order_id": order.id})
    return order


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: DbSession, redis_client: RedisClient) -> dict[str, Any]:
    """Read an order from Redis first, then PostgreSQL on cache miss."""
    try:
        cached = get_cached_order(redis_client, order_id)
    except (RedisError, ValueError, TypeError) as exc:
        cached = None
        logger.exception(
            "order_cache_read_failed",
            extra={"event": "order_cache_read_failed", "order_id": order_id, "error": str(exc)},
        )

    if cached:
        ORDER_CACHE_HITS.inc()
        logger.info("order_cache_hit", extra={"event": "order_cache_hit", "order_id": order_id})
        return cached

    ORDER_CACHE_MISSES.inc()
    try:
        order = db.get(Order, order_id)
    except SQLAlchemyError as exc:
        logger.exception(
            "order_lookup_database_error",
            extra={"event": "order_lookup_database_error", "order_id": order_id, "error": str(exc)},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve order",
        ) from exc

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    result = order_to_dict(order)
    try:
        cache_order(redis_client, order.id, result, settings.order_cache_ttl_seconds)
    except (RedisError, ValueError, TypeError) as exc:
        logger.exception(
            "order_cache_write_failed",
            extra={"event": "order_cache_write_failed", "order_id": order.id, "error": str(exc)},
        )

    return result


@router.get("/orders", response_model=list[OrderResponse])
def list_orders(db: DbSession) -> list[Order]:
    """Return recent orders."""
    try:
        return db.query(Order).order_by(Order.id.desc()).limit(50).all()
    except SQLAlchemyError as exc:
        logger.exception("order_list_database_error", extra={"event": "order_list_database_error"})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve orders",
        ) from exc
