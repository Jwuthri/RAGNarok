import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from datetime import datetime

from src.repositories.chat import ChatRepository
from src.db.chat import ChatTable
from src.schemas.chat import ChatSchema


@pytest.fixture
def mock_db_session():
    """Fixture to provide a mocked database session."""
    return create_autospec(Session, instance=True, spec_set=True)


@pytest.fixture
def chat_data():
    """Provides a sample ChatSchema data for testing."""
    return ChatSchema(
        id="1",
        users=["user1", "user2"],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        messages=[],
    )


def test_create_chat(mock_db_session, chat_data):
    """Test the create method of ChatRepository."""
    repository = ChatRepository(mock_db_session)
    repository.create(chat_data)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()


def test_read_chat_exists(mock_db_session, chat_data):
    """Test reading an existing Chat record."""
    mock_db_session.query.return_value.filter.return_value.first.return_value = chat_data

    repository = ChatRepository(mock_db_session)
    result = repository.read(chat_data.id)

    assert result == chat_data
    mock_db_session.query().filter().first.assert_called_once()


def test_read_chat_not_exists(mock_db_session):
    """Test reading a Chat record that does not exist."""
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    repository = ChatRepository(mock_db_session)
    result = repository.read(999)

    assert result is None


def test_update_chat_exists(mock_db_session, chat_data):
    """Test updating an existing Chat record."""
    updated_data = chat_data.copy(update={"messages": ["new message"]})
    mock_db_session.query.return_value.filter.return_value.first.return_value = updated_data

    repository = ChatRepository(mock_db_session)
    result = repository.update(chat_data.id, updated_data)

    assert result.messages == ["new message"]
    mock_db_session.commit.assert_called_once()


def test_delete_chat_exists(mock_db_session):
    """Test deleting an existing Chat record."""
    mock_db_session.query.return_value.filter.return_value.delete.return_value = 1

    repository = ChatRepository(mock_db_session)
    result = repository.delete(1)

    assert result == 1
    mock_db_session.commit.assert_called_once()


def test_delete_chat_not_exists(mock_db_session):
    """Test attempting to delete a Chat record that does not exist."""
    mock_db_session.query.return_value.filter.return_value.delete.return_value = 0

    repository = ChatRepository(mock_db_session)
    result = repository.delete(999)

    assert result == 0
    mock_db_session.commit.assert_called_once()