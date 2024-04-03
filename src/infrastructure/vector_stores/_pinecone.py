import time
import logging
from typing import Optional

from src.infrastructure.vector_stores.base import VectorStoreManager
from src import API_KEYS

logger = logging.getLogger(__name__)


class PineconeVectorStore(VectorStoreManager):
    def __init__(self) -> None:
        try:
            from pinecone import Pinecone

            self.connector = Pinecone(api_key=API_KEYS.PINECONE_API_KEY)
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install pinecone-client`")

    def create_index(
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

    def create(
        self,
        index_name: str,
        vectors: list,
        ids: Optional[list[str]] = None,
        async_req: Optional[bool] = False,
        namespace: Optional[str] = None,
    ):
        ...

    def read(
        self,
        index_name: str,
        ids: list,
        filters: Optional[dict] = None,
        async_req: Optional[bool] = False,
        namespace: Optional[str] = None,
    ):
        ...

    def upsert(self, index_name: str, vectors: list, async_req: Optional[bool], namespace: Optional[str]):
        ...

    def delete(
        self,
        index_name: str,
        ids: list,
        filters: Optional[dict] = None,
        async_req: Optional[bool] = False,
        namespace: Optional[str] = None,
    ):
        ...

    def get_session(self, index_name: str):
        return self.connector.Index(index_name)

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
