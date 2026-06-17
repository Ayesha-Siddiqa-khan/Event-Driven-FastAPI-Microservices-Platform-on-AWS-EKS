from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    service_name: str = "api-gateway"
    environment: str = "dev"
    auth_service_url: str = "http://localhost:8001"
    order_service_url: str = "http://localhost:8002"
    payment_service_url: str = "http://localhost:8003"
    request_timeout_seconds: float = Field(default=5.0, gt=0)
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
