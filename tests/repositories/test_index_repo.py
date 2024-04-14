import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from datetime import datetime

from src.repositories.index import IndexRepository
from src.schemas.index import IndexSchema


@pytest.fixture
def mock_db_session():
    """Fixture to provide a mocked database session."""
    return create_autospec(Session, instance=True, spec_set=True)


@pytest.fixture
def index_data():
    """Provides a sample IndexSchema data for testing."""
    return IndexSchema(
        text="Sample text for indexing", meta={"key": "value"}, created_at=datetime.now(), updated_at=datetime.now()
    )


def test_read_index_exists(mock_db_session, index_data):
    """Test reading an existing Index record."""
    mock_db_session.query.return_value.filter.return_value.first.return_value = index_data

    repository = IndexRepository(mock_db_session)
    result = repository.read(index_data.id)

    assert result == index_data
    mock_db_session.query().filter().first.assert_called_once()


def test_read_index_not_exists(mock_db_session):
    """Test reading an Index record that does not exist."""
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    repository = IndexRepository(mock_db_session)
    result = repository.read(999)

    assert result is None


def test_update_index_exists(mock_db_session, index_data):
    """Test updating an existing Index record."""
    updated_data = index_data.copy(update={"text": "Updated text"})
    mock_db_session.query.return_value.filter.return_value.first.return_value = updated_data

    repository = IndexRepository(mock_db_session)
    result = repository.update(index_data.id, updated_data)

    assert result.text == "Updated text"
    mock_db_session.commit.assert_called_once()


def test_delete_index_exists(mock_db_session):
    """Test deleting an existing Index record."""
    mock_db_session.query.return_value.filter.return_value.delete.return_value = 1

    repository = IndexRepository(mock_db_session)
    result = repository.delete(1)

    assert result == 1
    mock_db_session.commit.assert_called_once()


def test_delete_index_not_exists(mock_db_session):
    """Test attempting to delete an Index record that does not exist."""
    mock_db_session.query.return_value.filter.return_value.delete.return_value = 0

    repository = IndexRepository(mock_db_session)
    result = repository.delete(999)

    assert result == 0
    mock_db_session.commit.assert_called_once()
