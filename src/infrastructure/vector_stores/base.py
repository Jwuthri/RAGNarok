from typing import Optional, Callable, Any
from abc import ABC, abstractmethod
import logging
import math

from pydantic import BaseModel

from src.infrastructure.text_embedding.base import EmbeddingManager, EmbeddingType
from src.utils.file_utils import read_json_file

logger = logging.getLogger(__name__)


class Vector(BaseModel):
    id: str
    metadata: dict
    values: EmbeddingType
    sparse_values: Optional[dict[str, list[float]]] = None

    def model_dump(self) -> dict:
        metadata = self.metadata | {"__text__": self.values.text}
        data = {"id": self.id, "metadata": metadata, "values": self.values.embedding}
        if self.sparse_values:
            data["sparse_values"] = self.sparse_values

        return data


class VectorStoreManager(ABC):
    def __init__(self, embedding: EmbeddingManager, bm25_encoder: Optional[Callable] = None) -> None:
        self.embedding = embedding
        self.bm25_encoder = bm25_encoder

    def _embed_query(self, query: str) -> EmbeddingType:
        return self.embedding.embed_str(query)

    def _embed_queries(self, queries: list[str]) -> list[EmbeddingType]:
        return self.embedding.embed_batch(queries)

    def filter_from_args(self, **kwargs) -> dict[str, Any]:
        return {key: {self.filter_operators("=="): value} for key, value in kwargs.items() if value}

    @staticmethod
    def _euclidean_relevance_score_fn(distance: float) -> float:
        return 1.0 - distance / math.sqrt(2)

    @staticmethod
    def _cosine_relevance_score_fn(distance: float) -> float:
        return 1.0 - distance

    @staticmethod
    def _max_inner_product_relevance_score_fn(distance: float) -> float:
        if distance > 0:
            return 1.0 - distance

        return -1.0 * distance

    @staticmethod
    def load_bm25(path: str) -> dict:
        try:
            return read_json_file(path)
        except Exception as e:
            logger.error(e)
            raise e

    def fit_bm25(
        self,
        docs: list[str],
        b: float = 0.75,
        k1: float = 1.2,
        lower_case: bool = True,
        remove_punctuation: bool = True,
        remove_stopwords: bool = True,
        stem: bool = True,
        language: str = "english",
    ):
        try:
            from pinecone_text.sparse import BM25Encoder

            return BM25Encoder(b, k1, lower_case, remove_punctuation, remove_stopwords, stem, language).fit(docs)
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install pinecone-text`")

    @staticmethod
    @abstractmethod
    def filter_operators(operation: str) -> str:
        ...

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
    def create(self, index_name: str, dimension: int, metric: str, **kwargs):
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
    def upsert(self, index_name: str, vectors: list[Vector], async_req: Optional[bool], namespace: Optional[str]):
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
