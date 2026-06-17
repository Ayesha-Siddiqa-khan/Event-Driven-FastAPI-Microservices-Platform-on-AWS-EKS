import json
import logging

from app.config import settings

RESERVED_LOG_RECORD_KEYS = set(logging.makeLogRecord({}).__dict__)


class ServiceContextFilter(logging.Filter):
    """Attach service metadata to each log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.service = settings.service_name
        record.environment = settings.environment
        return True


class JsonFormatter(logging.Formatter):
    """Format log records as JSON for container-friendly logs."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "service": getattr(record, "service", settings.service_name),
            "environment": getattr(record, "environment", settings.environment),
            "event": getattr(record, "event", record.getMessage()),
            "message": record.getMessage(),
        }

        if record.exc_info:
            payload["error"] = self.formatException(record.exc_info)

        for key, value in record.__dict__.items():
            if key not in RESERVED_LOG_RECORD_KEYS and key not in payload:
                payload[key] = value

        return json.dumps(payload, default=str)


def configure_logging() -> None:
    logger = logging.getLogger()
    logger.setLevel(settings.log_level.upper())

    handler = logging.StreamHandler()
    handler.addFilter(ServiceContextFilter())
    handler.setFormatter(JsonFormatter())

    logger.handlers.clear()
    logger.addHandler(handler)
