from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

HTTP_REQUESTS = Counter(
    "payment_service_http_requests_total",
    "Total HTTP requests handled by payment-service",
    ["method", "path", "status_code"],
)
HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "payment_service_http_request_duration_seconds",
    "HTTP request duration in seconds for payment-service",
    ["method", "path"],
)
DEPENDENCY_READINESS_CHECKS = Counter(
    "payment_service_dependency_readiness_checks_total",
    "Dependency readiness check results",
    ["dependency", "status"],
)
PAYMENTS_CREATED = Counter("payment_service_payments_created_total", "Total payments created")
SUCCESSFUL_PAYMENTS = Counter("payment_service_successful_payments_total", "Total successful payments")
FAILED_PAYMENTS = Counter("payment_service_failed_payments_total", "Total failed payments")
SQS_MESSAGES_PUBLISHED = Counter(
    "payment_service_sqs_messages_published_total",
    "Total SQS messages published",
)
SQS_PUBLISH_FAILURES = Counter(
    "payment_service_sqs_publish_failures_total",
    "Total SQS publish failures",
)


def record_dependency_readiness(dependency: str, healthy: bool) -> None:
    """Track readiness success and failure counts per dependency."""
    DEPENDENCY_READINESS_CHECKS.labels(
        dependency=dependency,
        status="success" if healthy else "failure",
    ).inc()


def render_metrics() -> tuple[bytes, str]:
    """Render metrics in Prometheus exposition format."""
    return generate_latest(), CONTENT_TYPE_LATEST
