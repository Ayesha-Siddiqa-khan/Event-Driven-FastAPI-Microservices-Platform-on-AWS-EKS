from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

HTTP_REQUESTS = Counter(
    "order_service_http_requests_total",
    "Total HTTP requests handled by order-service",
    ["method", "path", "status_code"],
)
HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "order_service_http_request_duration_seconds",
    "HTTP request duration in seconds for order-service",
    ["method", "path"],
)
DEPENDENCY_READINESS_CHECKS = Counter(
    "order_service_dependency_readiness_checks_total",
    "Dependency readiness check results",
    ["dependency", "status"],
)
ORDERS_CREATED = Counter("order_service_orders_created_total", "Total orders created")
ORDER_CACHE_HITS = Counter("order_service_order_cache_hits_total", "Total order cache hits")
ORDER_CACHE_MISSES = Counter("order_service_order_cache_misses_total", "Total order cache misses")
SQS_MESSAGES_PUBLISHED = Counter(
    "order_service_sqs_messages_published_total",
    "Total SQS messages published",
)
SQS_PUBLISH_FAILURES = Counter(
    "order_service_sqs_publish_failures_total",
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
