from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

HTTP_REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status_code"],
)
HTTP_REQUEST_LATENCY_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
)
USER_REGISTRATIONS = Counter("user_registrations_total", "Total user registrations")
USER_LOGINS = Counter("user_logins_total", "Total successful user logins")
USER_LOGIN_FAILURES = Counter("user_login_failures_total", "Total failed user logins")
USER_LOOKUPS = Counter("user_lookups_total", "Total user lookup requests")


def render_metrics() -> tuple[bytes, str]:
    """Render metrics in Prometheus exposition format."""
    return generate_latest(), CONTENT_TYPE_LATEST
