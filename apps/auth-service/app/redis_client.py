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


redis_client = (
    redis.Redis.from_url(settings.redis_url, decode_responses=True)
    if redis is not None
    else MissingRedisClient()
)


def get_redis() -> Any:
    """Return the Redis client used for session storage."""
    return redis_client


def check_redis() -> bool:
    """Return True when Redis responds to PING."""
    try:
        return bool(redis_client.ping())
    except RedisError:
        logger.exception("redis_readiness_check_failed")
        return False
