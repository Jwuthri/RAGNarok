from typing import Optional, Callable
from pathlib import Path
from uuid import uuid4
import logging
import time

import numpy as np
from rich.progress import track

from ragnarok.core.text_embedding import OpenaiEmbedding, EmbeddingManager
from ragnarok.core.vector_stores.base import Vector, VectorStoreManager
from ragnarok.core.text_embedding.base import EmbeddingType
from ragnarok.schemas.models import EmbeddingOpenaiSmall3
from ragnarok.utils import dict_utils
from ragnarok import API_KEYS

logger = logging.getLogger(__name__)


class PineconeVectorStore(VectorStoreManager):
    def __init__(
        self,
        embedding: EmbeddingManager = None,
        bm25_encoder: Optional[Callable] = None,
        api_key: Optional[str] = API_KEYS.PINECONE_API_KEY,
    ):
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
        assert self.embedding is not None, "Please initialize the embedding"
        logger.info(f"Querying {query} from pinecone index:{index_name}")

        return self.similarity_search(
            index_name, self._embed_query(query).embedding, top_k, filters, async_req, namespace
        )

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
            vector=embedding, top_k=top_k, filter=filters, namespace=namespace, include_metadata=True
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
        bm25_path: Optional[str | Path] = None,
        namespace: Optional[str] = None,
        batch_size: Optional[int] = 32,
        async_req: Optional[bool] = False,
    ):
        assert self.embedding is not None, "Please initialize the embedding"
        assert len(docs) == len(metadata), "Please make sure docs, ids, and metadata are the same length"
        max_len = len(docs)
        sparse_embeddings = [None] * max_len
        if use_bm25:
            assert bm25_path, "please set the bm25_path (json file)"
            bm25 = self.fit_bm25(docs, namespace)
            sparse_embeddings = bm25.encode_documents(docs)
            bm25.dump(path=bm25_path)

        logger.info(f"Seeding {max_len} vectors in pinecone index:{index_name}")
        embeddings = self._embed_queries(docs)
        metadata = [dict_utils.flatten_dict(x) for x in metadata]
        metadata = [dict_utils.replace_none_values(x) for x in metadata]
        if not ids:
            ids = [str(uuid4()) for _ in range(max_len)]

        all_vectors: list[Vector] = [
            Vector(id=ids[i], metadata=metadata[i], values=embeddings[i], sparse_values=sparse_embeddings[i])
            for i in range(max_len)
        ]
        async_requests = []
        nb_chunks = max_len // batch_size
        for vectors in track(
            np.array_split(all_vectors, nb_chunks), description="Adding to pinecone index ....", total=nb_chunks
        ):
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
        logger.info(f"Creating {index_name} index in pinecone")
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
        logger.info(f"Reading {len(ids)} vectors in pinecone index:{index_name}")

        return self.get_session(index_name=index_name).fetch(ids=ids, namespace=namespace)

    def upsert(
        self, index_name: str, vectors: list[Vector], async_req: Optional[bool] = False, namespace: Optional[str] = None
    ):
        logger.info(f"Inserting {len(vectors)} vectors in pinecone index:{index_name}")

        return self.get_session(index_name=index_name).upsert(
            vectors=[v.model_dump() for v in vectors], async_req=async_req, namespace=namespace
        )

    def delete(
        self,
        index_name: str,
        ids: list,
        filters: Optional[dict] = None,
        async_req: Optional[bool] = False,
        namespace: Optional[str] = None,
    ):
        logger.info(f"Deleting vectors from pinecone index:{index_name}")

        return self.get_session(index_name=index_name).delete(
            ids=ids, delete_all=False, namespace=namespace, filter=filters
        )

    def delete_namespace(
        self,
        index_name: str,
        namespace: str,
        async_req: Optional[bool] = False,
    ):
        logger.info(f"Deleting namespace {namespace} from pinecone index:{index_name}")

        return self.get_session(index_name=index_name).delete(delete_all=True, namespace=namespace)


if __name__ == "__main__":
    pine = PineconeVectorStore(OpenaiEmbedding(EmbeddingOpenaiSmall3()))
    vectors = [Vector(id="id", metadata={"test": 1}, values=EmbeddingType(text="test", embedding=[0.1] * 1536))]
    pine.upsert(index_name=API_KEYS.PINECONE_INDEX, vectors=vectors)
    pine.delete(index_name=API_KEYS.PINECONE_INDEX, ids=["id"])
    docs = ["doc1", "doc2", "doc3", "doc4"]
    metadata = [{"test": 1}, {"test": 2}, {"test": 3}, {"test": 4}]
    pine.seed_index(index_name=API_KEYS.PINECONE_INDEX, docs=docs, metadata=metadata, batch_size=2)
