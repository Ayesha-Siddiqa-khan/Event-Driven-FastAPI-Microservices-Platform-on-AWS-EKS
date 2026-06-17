import logging
import time

from fastapi import FastAPI, Request, Response, status

from app.config import settings
from app.database import check_database
from app.logging_config import configure_logging
from app.metrics import (
    HTTP_REQUEST_DURATION_SECONDS,
    HTTP_REQUESTS,
    record_dependency_readiness,
    render_metrics,
)
from app.redis_client import check_redis
from app.routes import router
from app.sqs_client import check_sqs

configure_logging()
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title=settings.service_name)
    app.include_router(router)

    @app.middleware("http")
    async def record_requests(request: Request, call_next):
        started_at = time.perf_counter()
        response = await call_next(request)
        duration_seconds = time.perf_counter() - started_at
        route = request.scope.get("route")
        path = getattr(route, "path", request.url.path)

        HTTP_REQUESTS.labels(
            method=request.method,
            path=path,
            status_code=str(response.status_code),
        ).inc()
        HTTP_REQUEST_DURATION_SECONDS.labels(method=request.method, path=path).observe(duration_seconds)
        logger.info(
            "request_completed",
            extra={
                "event": "request_completed",
                "method": request.method,
                "path": path,
                "status_code": response.status_code,
                "duration_ms": round(duration_seconds * 1000, 2),
            },
        )
        return response

    @app.get("/health")
    def health() -> dict[str, str]:
        """Return liveness status for the service process."""
        return {
            "status": "ok",
            "service": settings.service_name,
            "environment": settings.environment,
        }

    @app.get("/ready")
    def ready(response: Response) -> dict[str, object]:
        """Return readiness status for PostgreSQL, Redis, and SQS."""
        raw_checks = {
            "postgres": check_database(),
            "redis": check_redis(),
            "sqs": check_sqs(),
        }
        for dependency, healthy in raw_checks.items():
            record_dependency_readiness(dependency, healthy)

        checks = {dependency: "ok" if healthy else "failed" for dependency, healthy in raw_checks.items()}
        ready_status = all(raw_checks.values())
        if not ready_status:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "ready" if ready_status else "not_ready", "checks": checks}

    @app.get("/metrics", include_in_schema=False)
    def metrics() -> Response:
        """Return Prometheus metrics."""
        body, media_type = render_metrics()
        return Response(content=body, media_type=media_type)

    return app


app = create_app()
