from abc import ABC, abstractmethod


class CacheManager(ABC):
    def __init__(self):
        self._cache = {}

    @abstractmethod
    def get(self, key):
        ...

    @abstractmethod
    def set(self, key, value):
        ...

    @abstractmethod
    def remove(self, key):
        ...

    @abstractmethod
    def clear(self):
        ...

    @abstractmethod
    def __len__(self) -> int:
        ...

    @abstractmethod
    def __contains__(self, key):
        ...
