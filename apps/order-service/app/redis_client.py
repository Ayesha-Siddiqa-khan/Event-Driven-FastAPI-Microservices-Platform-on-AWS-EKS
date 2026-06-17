import json
import logging
from typing import Any

try:
    import redis
    from redis.exceptions import RedisError
except ModuleNotFoundError:
    redis = None

    class RedisError(Exception):
        pass

from app.config import settings

logger = logging.getLogger(__name__)


class MissingRedisClient:
    """Placeholder client used when the redis package is not installed."""

    def ping(self) -> bool:
        raise RedisError("redis package is not installed")

    def setex(self, key: str, ttl: int, value: str) -> bool:
        raise RedisError("redis package is not installed")

    def get(self, key: str) -> str | None:
        raise RedisError("redis package is not installed")


redis_client = (
    redis.Redis.from_url(settings.redis_url, decode_responses=True)
    if redis is not None
    else MissingRedisClient()
)


def get_redis() -> Any:
    """Return the Redis client used for order cache access."""
    return redis_client


def check_redis() -> bool:
    """Return True when Redis responds to PING."""
    try:
        return bool(redis_client.ping())
    except RedisError:
        logger.exception("redis_readiness_check_failed", extra={"event": "redis_readiness_check_failed"})
        return False


def order_cache_key(order_id: int) -> str:
    """Return the Redis cache key for an order."""
    return f"order:{order_id}"


def cache_order(client: Any, order_id: int, payload: dict[str, Any], ttl_seconds: int) -> None:
    """Store an order payload in Redis as JSON."""
    client.setex(order_cache_key(order_id), ttl_seconds, json.dumps(payload, default=str))


def get_cached_order(client: Any, order_id: int) -> dict[str, Any] | None:
    """Return a cached order payload from Redis if it exists."""
    value = client.get(order_cache_key(order_id))
    if not value:
        return None
    return json.loads(value)
