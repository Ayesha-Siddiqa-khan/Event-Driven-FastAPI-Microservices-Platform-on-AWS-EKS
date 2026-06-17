from threading import Event, Thread
from fastapi import FastAPI, Response, status
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response as StarletteResponse
from app.config import settings
from app.database import check_database
from app.logging_config import configure_logging
from app.sqs_client import check_sqs
from app.worker import run_worker

configure_logging()

app = FastAPI(title=settings.service_name)
stop_event = Event()
worker_thread: Thread | None = None


@app.on_event("startup")
def start_worker():
    global worker_thread
    worker_thread = Thread(target=run_worker, args=(stop_event,), daemon=True)
    worker_thread.start()


@app.on_event("shutdown")
def stop_worker():
    stop_event.set()
    if worker_thread:
        worker_thread.join(timeout=10)


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.service_name, "environment": settings.environment}


@app.get("/ready")
def ready(response: Response):
    checks = {
        "postgres": "ok" if check_database() else "failed",
        "sqs": "ok" if check_sqs() else "failed",
    }
    ready_status = all(value == "ok" for value in checks.values())
    if not ready_status:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "ready" if ready_status else "not_ready", "checks": checks}


@app.get("/metrics")
def metrics():
    return StarletteResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
