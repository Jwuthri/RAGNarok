from typing import Optional

from langchain.vectorstores.base import VectorStore


class VectorStoreBase(VectorStore):
    def __init__(self) -> None:
        super().__init__()

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

    def upsert(self, vectors: list, async_req: Optional[bool], namespace: Optional[str]):
        ...
