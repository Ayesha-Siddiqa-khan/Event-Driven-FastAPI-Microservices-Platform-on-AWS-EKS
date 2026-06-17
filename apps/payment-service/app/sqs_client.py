import json
import logging
from typing import Any

try:
    import boto3
except ModuleNotFoundError:
    boto3 = None

from app.config import settings
from app.metrics import SQS_MESSAGES_PUBLISHED, SQS_PUBLISH_FAILURES
from app.models import PaymentStatus

logger = logging.getLogger(__name__)


class SqsError(Exception):
    """Raised when SQS is unavailable or rejects a publish request."""


class MissingSqsClient:
    """Placeholder client used when boto3 is not installed."""

    def send_message(self, **kwargs: Any) -> dict[str, Any]:
        raise SqsError("boto3 package is not installed")

    def get_queue_attributes(self, **kwargs: Any) -> dict[str, Any]:
        raise SqsError("boto3 package is not installed")


def build_payment_completed_message(
    order_id: int,
    payment_id: int,
    status: PaymentStatus | str,
) -> dict[str, str]:
    """Build the payment_completed event payload sent to SQS."""
    return {
        "event_type": "payment_completed",
        "order_id": str(order_id),
        "payment_id": str(payment_id),
        "status": str(status.value if isinstance(status, PaymentStatus) else status),
    }


def serialize_payment_completed_message(order_id: int, payment_id: int, status: PaymentStatus | str) -> str:
    """Serialize the payment_completed event payload as compact JSON."""
    return json.dumps(build_payment_completed_message(order_id, payment_id, status), separators=(",", ":"))


def get_sqs_client() -> Any:
    """Return a boto3 SQS client configured from environment variables."""
    if boto3 is None:
        return MissingSqsClient()

    kwargs = {"region_name": settings.aws_region}
    if settings.sqs_endpoint_url:
        kwargs["endpoint_url"] = settings.sqs_endpoint_url
    return boto3.client("sqs", **kwargs)


def publish_payment_completed(client: Any, order_id: int, payment_id: int, status: PaymentStatus | str) -> None:
    """Publish a payment_completed event to SQS."""
    if not settings.notification_events_queue_url:
        SQS_PUBLISH_FAILURES.inc()
        raise RuntimeError("NOTIFICATION_EVENTS_QUEUE_URL is not configured")

    try:
        client.send_message(
            QueueUrl=settings.notification_events_queue_url,
            MessageBody=serialize_payment_completed_message(order_id, payment_id, status),
        )
        SQS_MESSAGES_PUBLISHED.inc()
    except Exception as exc:
        SQS_PUBLISH_FAILURES.inc()
        logger.exception(
            "sqs_publish_failed",
            extra={
                "event": "sqs_publish_failed",
                "order_id": order_id,
                "payment_id": payment_id,
                "payment_status": str(status),
                "error": str(exc),
            },
        )
        raise SqsError("Could not publish payment_completed event") from exc


def check_sqs() -> bool:
    """Return True when the configured SQS queue can be queried."""
    try:
        if not settings.notification_events_queue_url:
            return False
        get_sqs_client().get_queue_attributes(
            QueueUrl=settings.notification_events_queue_url,
            AttributeNames=["QueueArn"],
        )
        return True
    except Exception as exc:
        logger.exception(
            "sqs_readiness_check_failed",
            extra={"event": "sqs_readiness_check_failed", "error": str(exc)},
        )
        return False
