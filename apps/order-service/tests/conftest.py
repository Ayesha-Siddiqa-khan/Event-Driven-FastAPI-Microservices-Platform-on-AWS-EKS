from collections.abc import Generator
from pathlib import Path
import json
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
from app.redis_client import get_redis  # noqa: E402
from app.sqs_client import get_sqs_client  # noqa: E402


class FakeRedis:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}
        self.ttls: dict[str, int] = {}

    def ping(self) -> bool:
        return True

    def setex(self, key: str, ttl: int, value: str) -> bool:
        self.values[key] = value
        self.ttls[key] = ttl
        return True

    def get(self, key: str) -> str | None:
        return self.values.get(key)

    def get_json(self, key: str) -> dict[str, Any] | None:
        value = self.get(key)
        return json.loads(value) if value else None


class FakeSqs:
    def __init__(self) -> None:
        self.messages: list[dict[str, Any]] = []

    def send_message(self, **kwargs: Any) -> dict[str, str]:
        self.messages.append(kwargs)
        return {"MessageId": "test-message-id"}

    def get_queue_attributes(self, **kwargs: Any) -> dict[str, Any]:
        return {"Attributes": {"QueueArn": "arn:aws:sqs:us-east-1:000000000000:order-events"}}


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
def fake_redis() -> FakeRedis:
    return FakeRedis()


@pytest.fixture()
def fake_sqs() -> FakeSqs:
    return FakeSqs()


@pytest.fixture()
def client(
    db_session: Session,
    fake_redis: FakeRedis,
    fake_sqs: FakeSqs,
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[TestClient, None, None]:
    monkeypatch.setattr(settings, "order_events_queue_url", "http://sqs.local/queue/order-events")

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    def override_get_redis() -> FakeRedis:
        return fake_redis

    def override_get_sqs_client() -> FakeSqs:
        return fake_sqs

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis
    app.dependency_overrides[get_sqs_client] = override_get_sqs_client

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
