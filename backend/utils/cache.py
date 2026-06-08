from typing import Any, Callable, TypeVar, Optional
from functools import wraps
import asyncio
from datetime import datetime, UTC, timedelta
import hashlib
import json

T = TypeVar("T")


class CacheEntry:
    def __init__(self, value: Any, ttl_seconds: int = 3600):
        self.value = value
        self.created_at = datetime.now(UTC)
        self.ttl_seconds = ttl_seconds

    def is_expired(self) -> bool:
        return (datetime.now(UTC) - self.created_at).total_seconds() > self.ttl_seconds


class MemoryCache:
    """Simple in-memory cache with TTL support"""

    def __init__(self):
        self._cache: dict[str, CacheEntry] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key not in self._cache:
            return None

        entry = self._cache[key]
        if entry.is_expired():
            async with self._lock:
                del self._cache[key]
            return None

        return entry.value

    async def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        """Set value in cache with TTL"""
        async with self._lock:
            self._cache[key] = CacheEntry(value, ttl_seconds)

    async def delete(self, key: str) -> None:
        """Delete value from cache"""
        async with self._lock:
            if key in self._cache:
                del self._cache[key]

    async def clear(self) -> None:
        """Clear entire cache"""
        async with self._lock:
            self._cache.clear()

    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_data = f"{prefix}:{str(args)}:{json.dumps(kwargs, sort_keys=True, default=str)}"
        return hashlib.md5(key_data.encode()).hexdigest()


# Global cache instance
_cache = MemoryCache()


def async_cached(ttl_seconds: int = 3600, key_prefix: str = "cache"):
    """Decorator for caching async function results"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = _cache._generate_key(key_prefix, *args, **kwargs)

            # Try to get from cache
            cached_value = await _cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Call original function
            result = await func(*args, **kwargs)

            # Store in cache
            await _cache.set(cache_key, result, ttl_seconds)

            return result

        return wrapper

    return decorator


def get_cache() -> MemoryCache:
    """Get global cache instance"""
    return _cache
