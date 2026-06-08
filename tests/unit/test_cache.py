"""Tests for caching functionality"""

import pytest
import asyncio
from backend.utils.cache import MemoryCache, get_cache


class TestMemoryCache:
    """Test memory cache functionality"""

    @pytest.mark.asyncio
    async def test_cache_set_and_get(self):
        """Test setting and getting values"""
        cache = MemoryCache()
        await cache.set("key1", "value1")
        result = await cache.get("key1")
        assert result == "value1"

    @pytest.mark.asyncio
    async def test_cache_get_nonexistent(self):
        """Test getting non-existent key"""
        cache = MemoryCache()
        result = await cache.get("nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_cache_delete(self):
        """Test deleting values"""
        cache = MemoryCache()
        await cache.set("key1", "value1")
        await cache.delete("key1")
        result = await cache.get("key1")
        assert result is None

    @pytest.mark.asyncio
    async def test_cache_clear(self):
        """Test clearing entire cache"""
        cache = MemoryCache()
        await cache.set("key1", "value1")
        await cache.set("key2", "value2")
        await cache.clear()
        assert await cache.get("key1") is None
        assert await cache.get("key2") is None

    @pytest.mark.asyncio
    async def test_cache_ttl_expiration(self):
        """Test TTL expiration"""
        cache = MemoryCache()
        await cache.set("key1", "value1", ttl_seconds=1)

        # Should exist immediately
        assert await cache.get("key1") == "value1"

        # Wait for expiration
        await asyncio.sleep(1.1)

        # Should be expired
        assert await cache.get("key1") is None

    def test_cache_key_generation(self):
        """Test cache key generation"""
        cache = MemoryCache()
        key1 = cache._generate_key("test", "arg1", kwarg="value")
        key2 = cache._generate_key("test", "arg1", kwarg="value")

        # Same args should produce same key
        assert key1 == key2

    def test_global_cache_instance(self):
        """Test global cache instance"""
        cache1 = get_cache()
        cache2 = get_cache()

        # Should be same instance
        assert cache1 is cache2
