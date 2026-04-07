import hashlib
import json
from collections.abc import Awaitable, Callable
from typing import Any

from redis.asyncio import Redis

CACHE_TTL = {
    "discover": 3600 * 6,
    "details": 3600 * 24,
    "providers": 3600 * 24,
    "credits": 3600 * 24 * 7,
    "trailer": 3600 * 24 * 7,
    "soundtrack": 3600 * 24 * 7,
}


def discover_key(filters: dict[str, Any]) -> str:
    payload = json.dumps(filters, sort_keys=True)
    return f"tmdb:discover:{hashlib.md5(payload.encode()).hexdigest()}"


async def get_or_set(redis: Redis, key: str, ttl: int, fetcher: Callable[[], Awaitable[Any]]) -> Any:
    cached = await redis.get(key)
    if cached:
        return json.loads(cached)
    value = await fetcher()
    await redis.setex(key, ttl, json.dumps(value))
    return value
