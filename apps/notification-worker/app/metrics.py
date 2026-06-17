from prometheus_client import Counter, Histogram

WORKER_MESSAGES_PROCESSED = Counter("worker_messages_processed_total", "Total worker messages processed")
WORKER_MESSAGES_FAILED = Counter("worker_messages_failed_total", "Total worker message processing failures")
WORKER_PROCESSING_SECONDS = Histogram("worker_processing_duration_seconds", "Worker message processing duration")
SQS_MESSAGES_CONSUMED = Counter("sqs_messages_consumed_total", "Total SQS messages consumed")
