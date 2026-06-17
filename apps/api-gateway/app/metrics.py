from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

HTTP_REQUESTS = Counter(
    "api_gateway_http_requests_total",
    "Total HTTP requests handled by api-gateway",
    ["method", "path", "status_code"],
)
HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "api_gateway_http_request_duration_seconds",
    "HTTP request duration in seconds for api-gateway",
    ["method", "path"],
)
UPSTREAM_REQUESTS = Counter(
    "api_gateway_upstream_requests_total",
    "Total upstream service requests",
    ["upstream_service", "method", "path", "status_code"],
)
UPSTREAM_FAILURES = Counter(
    "api_gateway_upstream_failures_total",
    "Total upstream service failures",
    ["upstream_service", "failure_type"],
)
READINESS_CHECKS = Counter(
    "api_gateway_readiness_checks_total",
    "Internal service readiness check results",
    ["upstream_service", "status"],
)


def record_upstream_request(upstream_service: str, method: str, path: str, status_code: int) -> None:
    """Track a completed upstream request."""
    UPSTREAM_REQUESTS.labels(
        upstream_service=upstream_service,
        method=method,
        path=path,
        status_code=str(status_code),
    ).inc()


def record_upstream_failure(upstream_service: str, failure_type: str) -> None:
    """Track timeout, unavailable, and error responses from upstream services."""
    UPSTREAM_FAILURES.labels(upstream_service=upstream_service, failure_type=failure_type).inc()


def record_readiness(upstream_service: str, healthy: bool) -> None:
    """Track readiness check success and failure."""
    READINESS_CHECKS.labels(
        upstream_service=upstream_service,
        status="success" if healthy else "failure",
    ).inc()


def render_metrics() -> tuple[bytes, str]:
    """Render metrics in Prometheus exposition format."""
    return generate_latest(), CONTENT_TYPE_LATEST
