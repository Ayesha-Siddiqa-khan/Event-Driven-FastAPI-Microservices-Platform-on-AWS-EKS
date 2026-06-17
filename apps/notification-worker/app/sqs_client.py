import boto3
from app.config import settings


def get_sqs_client():
    kwargs = {"region_name": settings.aws_region}
    if settings.sqs_endpoint_url:
        kwargs["endpoint_url"] = settings.sqs_endpoint_url
    return boto3.client("sqs", **kwargs)


def check_sqs() -> bool:
    try:
        if not settings.notification_events_queue_url:
            return False
        get_sqs_client().get_queue_attributes(
            QueueUrl=settings.notification_events_queue_url,
            AttributeNames=["ApproximateNumberOfMessages"],
        )
        return True
    except Exception:
        return False
