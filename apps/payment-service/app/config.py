from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    service_name: str = "payment-service"
    environment: str = "dev"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/devops_lab"
    aws_region: str = "us-east-1"
    notification_events_queue_url: str = ""
    sqs_endpoint_url: str | None = None
    payment_success_mode: Literal["always", "random"] = "always"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings so imports share one environment snapshot."""
    return Settings()


settings = get_settings()
