import pytest
from unittest.mock import MagicMock, ANY, patch

from src.infrastructure.vector_stores.base import Vector
from src.infrastructure.vector_stores._pinecone import PineconeVectorStore, OpenaiEmbedding


@pytest.fixture
def pinecone_vector_store():
    embedding = MagicMock(spec=OpenaiEmbedding)
    pinecone_store = PineconeVectorStore(embedding=embedding)

    return pinecone_store


@pytest.fixture
def mock_pinecone(pinecone_vector_store):
    mock_connector = MagicMock()
    pinecone_vector_store.connector = mock_connector

    return mock_connector


def test_create_index_success(pinecone_vector_store, mock_pinecone):
    from pinecone import PodSpec

    index_name = "test_index"
    dimension = 1536
    metric = "cosine"

    mock_connector_instance = mock_pinecone
    mock_connector_instance.create_index.return_value = True

    pinecone_vector_store.create(index_name=index_name, dimension=dimension, metric=metric)
    mock_connector_instance.create_index.assert_called_once_with(
        index_name,
        dimension=dimension,
        metric=metric,
        spec=PodSpec(
            environment="gcp-starter", replicas=None, shards=None, pods=None, pod_type="p1.x1", metadata_config={}
        ),
    )


def test_upsert_vectors(pinecone_vector_store, mock_pinecone):
    index_name = "test_index"
    vectors = [MagicMock(spec=Vector)]

    mock_session = MagicMock()
    mock_connector_instance = mock_pinecone
    mock_connector_instance.Index.return_value = mock_session
    mock_session.upsert.return_value = True

    pinecone_vector_store.upsert(index_name=index_name, vectors=vectors)
    mock_session.upsert.assert_called_once()


def test_query_success(pinecone_vector_store, mock_pinecone):
    index_name = "test_index"
    query_str = "search query"
    top_k = 5

    mock_session = MagicMock()
    mock_connector_instance = mock_pinecone
    mock_connector_instance.Index.return_value = mock_session
    mock_session.query.return_value = "query result"

    result = pinecone_vector_store.query(index_name=index_name, query=query_str, top_k=top_k)

    assert result == "query result"
    mock_session.query.assert_called_once_with(ANY, top_k=top_k, filter=None, namespace=None, include_metadata=True)


def test_similarity_search_success(pinecone_vector_store, mock_pinecone):
    index_name = "test_index"
    embedding = [0.1] * 128
    top_k = 10

    mock_session = MagicMock()
    mock_connector_instance = mock_pinecone
    mock_connector_instance.Index.return_value = mock_session
    mock_session.query.return_value = "search result"
    result = pinecone_vector_store.similarity_search(index_name=index_name, embedding=embedding, top_k=top_k)

    assert result == "search result"
    mock_session.query.assert_called_once_with(
        embedding, top_k=top_k, filter=None, namespace=None, include_metadata=True
    )


def test_delete_success(pinecone_vector_store, mock_pinecone):
    index_name = "test_index"
    ids = ["id1", "id2"]

    mock_session = MagicMock()
    mock_connector_instance = mock_pinecone
    mock_connector_instance.Index.return_value = mock_session
    mock_session.delete.return_value = True

    pinecone_vector_store.delete(index_name=index_name, ids=ids)
    mock_session.delete.assert_called_once_with(ids=ids, delete_all=False, namespace=None, filter=None)


def test_seed_index_success(pinecone_vector_store, mock_pinecone):
    index_name = "test_index"
    docs = ["doc1", "doc2"]
    metadata = [{"meta1": "data1"}, {"meta2": "data2"}]

    mock_embedding_method = MagicMock()
    mock_embedding_method.return_value = [
        {"embedding": [0.1, 0.2, 0.3], "text": "doc1"},
        {"embedding": [0.1, 0.2, 0.3], "text": "doc2"},
    ]
    with patch.object(pinecone_vector_store, "_embed_queries", mock_embedding_method):
        mock_upsert = MagicMock()
        pinecone_vector_store.upsert = mock_upsert
        pinecone_vector_store.seed_index(index_name=index_name, docs=docs, metadata=metadata, batch_size=2)

    assert mock_upsert.call_count >= 1
