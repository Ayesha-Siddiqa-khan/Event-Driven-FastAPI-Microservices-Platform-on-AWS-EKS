import logging
import time

from fastapi import FastAPI, Request

from app.config import settings
from app.logging_config import configure_logging
from app.metrics import HTTP_REQUEST_DURATION_SECONDS, HTTP_REQUESTS
from app.routes.gateway import router as gateway_router
from app.routes.health import router as health_router

configure_logging()
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title=settings.service_name)
    app.include_router(health_router)
    app.include_router(gateway_router)

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

    return app


app = create_app()
