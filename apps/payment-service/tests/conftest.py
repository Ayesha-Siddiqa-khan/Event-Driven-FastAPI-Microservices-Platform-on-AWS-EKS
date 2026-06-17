from collections.abc import Generator
from pathlib import Path
import sys
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

SERVICE_ROOT = Path(__file__).resolve().parents[1]
if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))

from app.config import settings  # noqa: E402
from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.sqs_client import get_sqs_client  # noqa: E402


class FakeSqs:
    def __init__(self) -> None:
        self.messages: list[dict[str, Any]] = []

    def send_message(self, **kwargs: Any) -> dict[str, str]:
        self.messages.append(kwargs)
        return {"MessageId": "test-message-id"}

    def get_queue_attributes(self, **kwargs: Any) -> dict[str, Any]:
        return {"Attributes": {"QueueArn": "arn:aws:sqs:us-east-1:000000000000:notification-events"}}


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as session:
        yield session

    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def fake_sqs() -> FakeSqs:
    return FakeSqs()


@pytest.fixture()
def client(
    db_session: Session,
    fake_sqs: FakeSqs,
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[TestClient, None, None]:
    monkeypatch.setattr(settings, "notification_events_queue_url", "http://sqs.local/queue/notification-events")
    monkeypatch.setattr(settings, "payment_success_mode", "always")

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    def override_get_sqs_client() -> FakeSqs:
        return fake_sqs

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_sqs_client] = override_get_sqs_client

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
