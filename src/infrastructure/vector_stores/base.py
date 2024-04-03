from abc import ABC, abstractmethod
from typing import Optional


class VectorStoreManager(ABC):
    @abstractmethod
    def seed_index(
        self,
        index_name: str,
        docs: list[str],
        metadata: list,
        use_bm25: Optional[bool] = False,
        namespace: Optional[str] = None,
        batch_size: Optional[int] = 32,
        async_req: Optional[bool] = False,
    ):
        ...

    @abstractmethod
    def get_session(self, index_name: str):
        ...

    @abstractmethod
    def create_index(self, index_name: str, dimension: int, metric: str, **kwargs):
        ...

    @abstractmethod
    def create(
        self,
        index_name: str,
        vectors: list,
        ids: Optional[list[str]] = None,
        async_req: Optional[bool] = False,
        namespace: Optional[str] = None,
    ):
        ...

    @abstractmethod
    def read(
        self,
        index_name: str,
        ids: list,
        filters: Optional[dict] = None,
        async_req: Optional[bool] = False,
        namespace: Optional[str] = None,
    ):
        ...

    @abstractmethod
    def upsert(self, index_name: str, vectors: list, async_req: Optional[bool], namespace: Optional[str]):
        ...

    @abstractmethod
    def delete(
        self,
        index_name: str,
        ids: list,
        filters: Optional[dict] = None,
        async_req: Optional[bool] = False,
        namespace: Optional[str] = None,
    ):
        ...
