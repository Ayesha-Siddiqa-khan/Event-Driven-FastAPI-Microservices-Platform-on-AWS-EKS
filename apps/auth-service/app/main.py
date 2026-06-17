import logging
import time

from fastapi import FastAPI, Request, Response, status

from app.config import settings
from app.database import check_database
from app.logging_config import configure_logging
from app.metrics import HTTP_REQUEST_LATENCY_SECONDS, HTTP_REQUESTS, render_metrics
from app.redis_client import check_redis
from app.routes import router

configure_logging()
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title=settings.service_name)
    app.include_router(router)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        started_at = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
        route = request.scope.get("route")
        path = getattr(route, "path", request.url.path)
        HTTP_REQUESTS.labels(
            method=request.method,
            path=path,
            status_code=str(response.status_code),
        ).inc()
        HTTP_REQUEST_LATENCY_SECONDS.labels(method=request.method, path=path).observe(duration_ms / 1000)
        logger.info(
            "request_completed",
            extra={
                "method": request.method,
                "path": path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
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

    @app.get("/metrics", include_in_schema=False)
    def metrics() -> Response:
        """Return Prometheus metrics."""
        body, media_type = render_metrics()
        return Response(content=body, media_type=media_type)

    @app.get("/ready")
    def ready(response: Response) -> dict[str, object]:
        """Return readiness status for PostgreSQL and Redis dependencies."""
        checks = {
            "postgres": "ok" if check_database() else "failed",
            "redis": "ok" if check_redis() else "failed",
        }
        ready_status = all(value == "ok" for value in checks.values())
        if not ready_status:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "ready" if ready_status else "not_ready", "checks": checks}

    return app


app = create_app()
