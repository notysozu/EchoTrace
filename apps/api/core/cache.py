import json
from typing import Any, Optional
import redis.asyncio as aioredis
from core.config import get_settings

settings = get_settings()

_redis: Optional[aioredis.Redis] = None


async def get_redis() -> aioredis.Redis:
    global _redis
    if _redis is None:
        _redis = aioredis.from_url(settings.redis_url, decode_responses=True)
    return _redis


class Cache:
    def __init__(self, prefix: str = "echotrace"):
        self.prefix = prefix

    def _key(self, key: str) -> str:
        return f"{self.prefix}:{key}"

    async def get(self, key: str) -> Optional[Any]:
        r = await get_redis()
        raw = await r.get(self._key(key))
        if raw:
            return json.loads(raw)
        return None

    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        r = await get_redis()
        await r.setex(self._key(key), ttl, json.dumps(value, default=str))

    async def delete(self, key: str) -> None:
        r = await get_redis()
        await r.delete(self._key(key))

    async def invalidate_pattern(self, pattern: str) -> None:
        r = await get_redis()
        keys = await r.keys(self._key(pattern))
        if keys:
            await r.delete(*keys)


cache = Cache()

# TTL constants (seconds)
TTL_TIMELINE = 300       # 5 min
TTL_EVENT = 900          # 15 min
TTL_AUDIO_META = 1800    # 30 min
TTL_PRESIGNED = 3000     # 50 min (URLs expire at 60 min)
TTL_USER_HISTORY = 120   # 2 min
