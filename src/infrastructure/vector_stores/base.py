from abc import ABC, abstractmethod
from typing import Optional


class VectorStoreManager(ABC):
    @abstractmethod
    def build_index(
        self,
        namespace: str,
        docs: list[str],
        metadata: list,
        use_bm25: bool,
        batch_size: int = 32,
        async_req: bool = False,
    ):
        ...

    @abstractmethod
    def upsert(self, vectors: list, async_req: Optional[bool], namespace: Optional[str]):
        ...
