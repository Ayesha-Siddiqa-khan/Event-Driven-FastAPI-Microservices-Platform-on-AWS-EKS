from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    service_name: str = "auth-service"
    environment: str = "dev"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/devops_lab"
    redis_url: str = "redis://localhost:6379/0"
    session_ttl_seconds: int = Field(default=3600, gt=0)
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
