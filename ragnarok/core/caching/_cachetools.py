import logging

from ragnarok.core.caching.base import CacheManager

logger = logging.getLogger(__name__)


class Cachetools(CacheManager):
    def __init__(self):
        try:
            from cachetools import TTLCache

            self.cache_func = TTLCache
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install cachetools`")

        self._cache = TTLCache(maxsize=4096, ttl=600)

    def get(self, key):
        return self._cache.get(key)

    def set(self, key, value):
        self._cache[key] = value

    def remove(self, key):
        del self._cache[key]

    def clear(self):
        self._cache = self.load_cache()

    def __len__(self) -> int:
        return len(self._cache)

    def __contains__(self, key):
        return key in self._cache

    def load_cache(self):
        self._cache = self.cache_func(maxsize=4096, ttl=600)
