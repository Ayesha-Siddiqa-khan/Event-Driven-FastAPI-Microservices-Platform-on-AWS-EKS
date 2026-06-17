import json
import logging
from decimal import Decimal
from typing import Any

try:
    import boto3
except ModuleNotFoundError:
    boto3 = None

from app.config import settings
from app.metrics import SQS_MESSAGES_PUBLISHED, SQS_PUBLISH_FAILURES

logger = logging.getLogger(__name__)


class SqsError(Exception):
    """Raised when SQS is unavailable or rejects a publish request."""


class MissingSqsClient:
    """Placeholder client used when boto3 is not installed."""

    def send_message(self, **kwargs: Any) -> dict[str, Any]:
        raise SqsError("boto3 package is not installed")

    def get_queue_attributes(self, **kwargs: Any) -> dict[str, Any]:
        raise SqsError("boto3 package is not installed")


def _json_number(amount: Decimal) -> int | float:
    normalized = amount.normalize()
    if normalized == normalized.to_integral_value():
        return int(normalized)
    return float(amount)


def build_order_created_message(order_id: int, user_id: int, amount: Decimal) -> dict[str, object]:
    """Build the order_created event payload sent to SQS."""
    return {
        "event_type": "order_created",
        "order_id": str(order_id),
        "user_id": str(user_id),
        "amount": _json_number(amount),
    }


def serialize_order_created_message(order_id: int, user_id: int, amount: Decimal) -> str:
    """Serialize the order_created event payload as compact JSON."""
    return json.dumps(build_order_created_message(order_id, user_id, amount), separators=(",", ":"))


def get_sqs_client() -> Any:
    """Return a boto3 SQS client configured from environment variables."""
    if boto3 is None:
        return MissingSqsClient()

    kwargs = {"region_name": settings.aws_region}
    if settings.sqs_endpoint_url:
        kwargs["endpoint_url"] = settings.sqs_endpoint_url
    return boto3.client("sqs", **kwargs)


def publish_order_created(client: Any, order_id: int, user_id: int, amount: Decimal) -> None:
    """Publish an order_created event to SQS."""
    if not settings.order_events_queue_url:
        SQS_PUBLISH_FAILURES.inc()
        raise RuntimeError("ORDER_EVENTS_QUEUE_URL is not configured")

    try:
        client.send_message(
            QueueUrl=settings.order_events_queue_url,
            MessageBody=serialize_order_created_message(order_id, user_id, amount),
        )
        SQS_MESSAGES_PUBLISHED.inc()
    except Exception as exc:
        SQS_PUBLISH_FAILURES.inc()
        logger.exception(
            "sqs_publish_failed",
            extra={"event": "sqs_publish_failed", "order_id": order_id, "error": str(exc)},
        )
        raise SqsError("Could not publish order_created event") from exc


def check_sqs() -> bool:
    """Return True when the configured SQS queue can be queried."""
    try:
        if not settings.order_events_queue_url:
            return False
        get_sqs_client().get_queue_attributes(
            QueueUrl=settings.order_events_queue_url,
            AttributeNames=["QueueArn"],
        )
        return True
    except Exception as exc:
        logger.exception(
            "sqs_readiness_check_failed",
            extra={"event": "sqs_readiness_check_failed", "error": str(exc)},
        )
        return False
