from src.infrastructure.caching.base import CacheManager


class MemoryCache(CacheManager):
    def __init__(self):
        super().__init__()

    def get(self, key):
        return self._cache.get(key)

    def set(self, key, value):
        self._cache[key] = value

    def remove(self, key):
        del self._cache[key]

    def clear(self):
        self._cache = {}

    def __len__(self) -> int:
        return len(self._cache)

    def __contains__(self, key):
        return key in self._cache

    def load_cache(self):
        self._cache = {}
