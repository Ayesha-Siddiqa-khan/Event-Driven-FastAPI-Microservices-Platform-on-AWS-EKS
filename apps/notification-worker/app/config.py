from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "notification-worker"
    environment: str = "dev"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/devops_lab"
    notification_events_queue_url: str = ""
    aws_region: str = "us-east-1"
    sqs_endpoint_url: str | None = None
    worker_poll_interval_seconds: int = 2
    sqs_wait_time_seconds: int = 10
    sqs_max_number_of_messages: int = 5

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
