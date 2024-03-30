import logging
from typing import Callable, Optional, Union

import pinecone
from pinecone_text.sparse import BM25Encoder
from tqdm.auto import tqdm
from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import Pinecone
from langchain.vectorstores.utils import DistanceStrategy
from kevin.const import PathsConfig, S3Buckets
from kevin.interface.commands.aws_filesystem import upload_file_s3
from kevin.utils.dict_utils import flatten_dict, replace_none_values

from kevin.utils.setup import set_up

pinecone.init(api_key=set_up()["PINECONE_API_KEY"], environment=set_up()["PINECONE_ENV"])
logger = logging.getLogger(__name__)


class PineconeVectorDB(Pinecone):
    def __init__(
        self,
        index: pinecone.Index,
        embedding: Union[Embeddings, Callable],
        text_key: str,
        namespace: Optional[str] = None,
        distance_strategy: Optional[DistanceStrategy] = DistanceStrategy.COSINE,
        embedding_dimension: int = 1536,
    ):
        super().__init__(index, embedding, text_key, namespace, distance_strategy)
        self.embedding_dimension = embedding_dimension

    def reconnect_pinecone(self, index_name: str, pool_threads: int = 4):
        self._index = pinecone.Index(index_name, pool_threads=pool_threads)

    @classmethod
    def get_pinecone_index(
        cls,
        index_name: str,
        dimension: Optional[int] = 1536,
        create_if_missing: bool = True,
        pool_threads: int = 4,
        metric: Optional[str] = DistanceStrategy.COSINE,
    ) -> pinecone.Index:
        return pinecone.Index(index_name)

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter: Optional[dict] = None,
        namespace: Optional[str] = None,
    ) -> list[tuple[Document, float]]:
        """Return pinecone documents most similar to query, along with scores."""
        return self.similarity_search_by_vector_with_score(
            self._embed_query(query), k=k, filter=filter, namespace=namespace
        )

    def similarity_search_by_vector_with_score(
        self,
        embedding: list[float],
        *,
        k: int = 4,
        filter: Optional[dict] = None,
        namespace: Optional[str] = None,
    ) -> list[tuple[Document, float]]:
        """Return pinecone documents most similar to embedding, along with scores."""
        if namespace is None:
            namespace = self._namespace
        docs = []
        results = self._index.query(
            [embedding],
            top_k=k,
            include_metadata=True,
            namespace=namespace,
            filter=filter,
        )
        for res in results["matches"]:
            metadata = res["metadata"]
            if self._text_key in metadata:
                text = metadata.pop(self._text_key)
                score = res["score"]
                docs.append((Document(page_content=text, metadata=metadata), score))
            else:
                logger.warning(f"Found document with no `{self._text_key}` key. Skipping.")

        return docs

    def upsert(self, vectors: list, async_req: Optional[bool], namespace: Optional[str]):
        self._index.upsert(vectors=vectors, async_req=async_req, namespace=namespace)

    def fit_bm25(self, docs: list[str], namespace: str) -> BM25Encoder:
        bm25 = BM25Encoder()
        bm25.fit(docs)
        bm25_filename = f"{namespace}_bm25.json"
        bm25_path = PathsConfig.bm25_path / bm25_filename
        bm25.dump(bm25_path)
        try:
            upload_file_s3(bucket=S3Buckets.bm25, filename=bm25_filename, path=bm25_path)
        except Exception as e:
            logger.error(e)
            logger.warning("please make sure you run `aws sso login`")

        return bm25

    def prepare_batch(
        self, start: int, end: int, metadata: list, embeddings: list, sparse_embeddings: list, use_bm25: bool
    ) -> list[dict]:
        _data_batch = metadata[start:end]
        dense_embeddings_batch = embeddings[start:end]
        sparse_embeddings_batch = sparse_embeddings[start:end]
        metadata_batch = [flatten_dict(x) for x in metadata]
        ids_batch = [x["id"] for x in _data_batch]
        vectors = []
        for _id, _sparse, _dense, _metadata in zip(
            ids_batch, sparse_embeddings_batch, dense_embeddings_batch, metadata_batch
        ):
            _metadata = replace_none_values(_metadata)
            vector = {"id": _id, "values": _dense, "metadata": _metadata}
            if use_bm25:
                vector["sparse_values"] = _sparse
            vectors.append(vector)

        return vectors

    def build_index(
        self,
        namespace: str,
        docs: list[str],
        metadata: list,
        use_bm25: bool,
        batch_size: int = 32,
        async_req: bool = False,
    ):
        max_len = len(docs)
        sparse_embeddings = [0] * max_len
        embeddings = self._embed_documents(docs)
        if use_bm25:
            bm25 = self.fit_bm25(docs, namespace)
            sparse_embeddings = bm25.encode_documents(docs)
        async_requests = []
        for start in tqdm(range(0, max_len, batch_size), desc="Adding to pinecone index ...."):
            end = min(start + batch_size, max_len)
            vectors = self.prepare_batch(start, end, metadata, embeddings, sparse_embeddings, use_bm25)
            async_requests.append(self.upsert(vectors=vectors, async_req=async_req, namespace=namespace))

        if async_req:
            [res.get() for res in async_requests]
