import time
import logging
from typing import Optional, Callable

from tqdm import tqdm
import numpy as np
from rich.progress import track

from src.infrastructure.text_embedding.base import EmbeddingManager
from src.infrastructure.vector_stores.base import VectorStoreManager
from src.utils import dict_utils
from src import API_KEYS

logger = logging.getLogger(__name__)


class PineconeVectorStore(VectorStoreManager):
    def __init__(
        self,
        embedding: EmbeddingManager,
        bm25_encoder: Optional[Callable] = None,
        api_key: Optional[str] = API_KEYS.PINECONE_API_KEY,
    ) -> None:
        super().__init__(embedding, bm25_encoder)
        try:
            from pinecone import Pinecone

            self.connector = Pinecone(api_key=api_key)
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install pinecone-client`")

    def query(
        self,
        index_name: str,
        query: str,
        top_k: int = 10,
        filters: Optional[dict] = None,
        async_req: Optional[bool] = False,
        namespace: Optional[str] = None,
    ):
        return self.similarity_search(index_name, self._embed_query(query), top_k, filters, async_req, namespace)

    def similarity_search(
        self,
        index_name: str,
        embedding: list[float],
        top_k: int = 10,
        filters: Optional[dict] = None,
        async_req: Optional[bool] = False,
        namespace: Optional[str] = None,
    ):
        return self.get_session(index_name=index_name).query(
            embedding, top_k=top_k, filter=filters, namespace=namespace, include_metadata=True
        )

    @staticmethod
    def filter_operators(operation: str) -> str:
        operator_mapping = {
            "==": "$eq",
            "!=": "$ne",
            ">": "$gt",
            "<": "$lt",
            ">=": "$gte",
            "<=": "$lte",
            "in": "$in",
            "not in": "$nin",
            "and": "$and",
            "or": "$or",
        }

        return operator_mapping.get(operation, operation)

    def get_session(self, index_name: str):
        return self.connector.Index(index_name)

    def seed_index(
        self,
        index_name: str,
        docs: list[str],
        metadata: list[dict],
        ids: Optional[list[str]] = None,
        use_bm25: Optional[bool] = False,
        namespace: Optional[str] = None,
        batch_size: Optional[int] = 32,
        async_req: Optional[bool] = False,
    ):
        max_len = len(docs)
        sparse_embeddings = [0] * max_len
        embeddings = self._embed_queries(docs)
        metadata = [dict_utils.flatten_dict(x) for x in metadata]
        metadata = [dict_utils.replace_none_values(x) for x in metadata]

        if use_bm25:
            bm25 = self.fit_bm25(docs, namespace)
            sparse_embeddings = bm25.encode_documents(docs)

        group = list(zip(docs, ids, metadata, embeddings, sparse_embeddings))
        async_requests = []
        nb_chunks = max_len // batch_size
        for chunk in track(np.array_split(group, nb_chunks), desc="Adding to pinecone index ....", total=nb_chunks):
            _docs, _ids, _metadata, _embeddings, _sparse_embeddings = chunk
            vectors = [
                {"id": _ids[i], "values": _embeddings[i], "metadata": _metadata[i]}
                | {"sparse_values": _sparse_embeddings[i]}
                if use_bm25
                else {}
                for i in range(len(_docs))
            ]
            async_requests.append(
                self.upsert(index_name=index_name, vectors=vectors, async_req=async_req, namespace=namespace)
            )
        [res.get() for res in async_requests] if async_req else None

    def create(
        self,
        index_name: str,
        dimension: int,
        metric: str,
        use_serverless: Optional[bool] = False,
        cloud: Optional[str] = "aws",
        region: Optional[str] = "us-west-2",
    ):
        from pinecone import ServerlessSpec, PodSpec

        if use_serverless:
            spec = ServerlessSpec(cloud=cloud, region=region)
        else:
            spec = PodSpec(environment=API_KEYS.PINECONE_ENV)
        self.connector.create_index(index_name, dimension=dimension, metric=metric, spec=spec)
        while not self.connector.describe_index(index_name).status["ready"]:
            time.sleep(1)

    def read(
        self,
        index_name: str,
        ids: list,
        async_req: Optional[bool] = False,
        namespace: Optional[str] = None,
    ):
        return self.get_session(index_name=index_name).fetch(ids=ids, namespace=namespace)

    def upsert(self, index_name: str, vectors: list, async_req: Optional[bool], namespace: Optional[str]):
        return self.get_session(index_name=index_name).upsert(vectors=vectors, async_req=async_req, namespace=namespace)

    def delete(
        self,
        index_name: str,
        ids: list,
        filters: Optional[dict] = None,
        async_req: Optional[bool] = False,
        namespace: Optional[str] = None,
    ):
        return self.get_session(index_name=index_name).delete(
            ids=ids, delete_all=False, namespace=namespace, filter=filters
        )

    def delete_namespace(
        self,
        index_name: str,
        namespace: str,
        async_req: Optional[bool] = False,
    ):
        return self.get_session(index_name=index_name).delete(delete_all=True, namespace=namespace)
