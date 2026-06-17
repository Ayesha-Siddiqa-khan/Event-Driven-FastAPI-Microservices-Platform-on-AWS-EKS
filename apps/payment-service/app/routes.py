import logging
import random
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.metrics import FAILED_PAYMENTS, PAYMENTS_CREATED, SUCCESSFUL_PAYMENTS
from app.models import Payment, PaymentStatus
from app.schemas import PaymentCreate, PaymentResponse
from app.sqs_client import SqsError, get_sqs_client, publish_payment_completed

logger = logging.getLogger(__name__)
router = APIRouter()

DbSession = Annotated[Session, Depends(get_db)]
SqsClient = Annotated[Any, Depends(get_sqs_client)]


def resolve_payment_status() -> PaymentStatus:
    """Resolve simulated payment status from PAYMENT_SUCCESS_MODE."""
    if settings.payment_success_mode == "random":
        return random.choice([PaymentStatus.SUCCESS, PaymentStatus.FAILED])
    return PaymentStatus.SUCCESS


def record_payment_metrics(payment_status: str) -> None:
    """Increment payment counters for a committed payment record."""
    PAYMENTS_CREATED.inc()
    if payment_status == PaymentStatus.SUCCESS.value:
        SUCCESSFUL_PAYMENTS.inc()
    else:
        FAILED_PAYMENTS.inc()


@router.post("/payments/{order_id}", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(
    order_id: Annotated[int, Path(gt=0)],
    payload: PaymentCreate,
    db: DbSession,
    sqs_client: SqsClient,
) -> Payment:
    """Create a simulated payment and publish a payment_completed event."""
    payment_status = resolve_payment_status()
    payment = Payment(order_id=order_id, amount=payload.amount, status=payment_status.value)

    try:
        db.add(payment)
        db.commit()
        db.refresh(payment)
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception(
            "payment_create_database_error",
            extra={"event": "payment_create_database_error", "order_id": order_id, "error": str(exc)},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create payment",
        ) from exc

    record_payment_metrics(payment.status)

    try:
        publish_payment_completed(sqs_client, order_id=order_id, payment_id=payment.id, status=payment.status)
    except (RuntimeError, SqsError) as exc:
        logger.exception(
            "payment_event_publish_failed",
            extra={
                "event": "payment_event_publish_failed",
                "order_id": order_id,
                "payment_id": payment.id,
                "payment_status": payment.status,
                "error": str(exc),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Payment event publishing unavailable",
        ) from exc

    logger.info(
        "payment_created",
        extra={
            "event": "payment_created",
            "order_id": order_id,
            "payment_id": payment.id,
            "payment_status": payment.status,
        },
    )
    return payment


@router.get("/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: Annotated[int, Path(gt=0)], db: DbSession) -> Payment:
    """Return a payment record by id."""
    try:
        payment = db.get(Payment, payment_id)
    except SQLAlchemyError as exc:
        logger.exception(
            "payment_lookup_database_error",
            extra={"event": "payment_lookup_database_error", "payment_id": payment_id, "error": str(exc)},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve payment",
        ) from exc

    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return payment
