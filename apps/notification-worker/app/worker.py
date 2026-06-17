import json
import logging
import time
from threading import Event
from app.config import settings
from app.database import SessionLocal
from app.metrics import (
    SQS_MESSAGES_CONSUMED,
    WORKER_MESSAGES_FAILED,
    WORKER_MESSAGES_PROCESSED,
    WORKER_PROCESSING_SECONDS,
)
from app.models import Notification
from app.sqs_client import get_sqs_client

logger = logging.getLogger(__name__)


def process_message(body: dict) -> None:
    order_id = int(body["order_id"])
    user_id = int(body["user_id"]) if body.get("user_id") else None
    status = body.get("status", "unknown")
    message = f"Payment status for order {order_id}: {status}"

    db = SessionLocal()
    try:
        notification = Notification(user_id=user_id, order_id=order_id, message=message, status="created")
        db.add(notification)
        db.commit()
    finally:
        db.close()


def run_worker(stop_event: Event) -> None:
    client = get_sqs_client()
    queue_url = settings.notification_events_queue_url
    if not queue_url:
        logger.error("NOTIFICATION_EVENTS_QUEUE_URL is not configured")
        return

    logger.info("notification-worker started")
    while not stop_event.is_set():
        try:
            response = client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=settings.sqs_max_number_of_messages,
                WaitTimeSeconds=settings.sqs_wait_time_seconds,
            )
            messages = response.get("Messages", [])
            if not messages:
                time.sleep(settings.worker_poll_interval_seconds)
                continue

            for message in messages:
                with WORKER_PROCESSING_SECONDS.time():
                    try:
                        SQS_MESSAGES_CONSUMED.inc()
                        body = json.loads(message["Body"])
                        process_message(body)
                        client.delete_message(QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"])
                        WORKER_MESSAGES_PROCESSED.inc()
                    except Exception as exc:
                        WORKER_MESSAGES_FAILED.inc()
                        logger.exception("failed to process message", extra={"error": str(exc)})
        except Exception as exc:
            WORKER_MESSAGES_FAILED.inc()
            logger.exception("worker polling error", extra={"error": str(exc)})
            time.sleep(settings.worker_poll_interval_seconds)

    logger.info("notification-worker stopped")
