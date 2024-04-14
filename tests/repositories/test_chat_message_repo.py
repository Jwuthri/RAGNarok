import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from datetime import datetime

from src.schemas.chat_message import ChatMessageSchema
from src.repositories.chat_message import ChatMessageRepository


@pytest.fixture
def mock_db_session():
    """Fixture to provide a mocked database session."""
    return create_autospec(Session, instance=True, spec_set=True)


@pytest.fixture
def chat_message_data():
    """Provides a sample ChatMessage data for testing."""
    return ChatMessageSchema(
        message="Test message", role="user", meta={"sample": "data"}, created_at=datetime.now(), chat_id="id"
    )


def test_create_chat_message(mock_db_session, chat_message_data):
    """Test the create method of ChatMessageRepository."""
    repository = ChatMessageRepository(mock_db_session)
    repository.create(chat_message_data)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()


def test_read_chat_message_exists(mock_db_session, chat_message_data):
    """Test reading an existing ChatMessage record."""
    mock_db_session.query.return_value.filter.return_value.first.return_value = chat_message_data

    repository = ChatMessageRepository(mock_db_session)
    result = repository.read(chat_message_data.id)

    assert result == chat_message_data
    mock_db_session.query().filter().first.assert_called_once()


def test_read_chat_message_not_exists(mock_db_session):
    """Test reading a ChatMessage record that does not exist."""
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    repository = ChatMessageRepository(mock_db_session)
    result = repository.read(999)

    assert result is None


def test_update_chat_message_exists(mock_db_session, chat_message_data):
    """Test updating an existing ChatMessage record."""
    updated_data = chat_message_data.copy(update={"message": "Updated message"})
    mock_db_session.query.return_value.filter.return_value.first.return_value = updated_data

    repository = ChatMessageRepository(mock_db_session)
    result = repository.update(chat_message_data.id, updated_data)

    assert result.message == "Updated message"
    mock_db_session.commit.assert_called_once()


def test_delete_chat_message_exists(mock_db_session):
    """Test deleting an existing ChatMessage record."""
    mock_db_session.query.return_value.filter.return_value.delete.return_value = 1

    repository = ChatMessageRepository(mock_db_session)
    result = repository.delete(1)

    assert result == 1
    mock_db_session.commit.assert_called_once()


def test_delete_chat_message_not_exists(mock_db_session):
    """Test attempting to delete a ChatMessage record that does not exist."""
    mock_db_session.query.return_value.filter.return_value.delete.return_value = 0

    repository = ChatMessageRepository(mock_db_session)
    result = repository.delete(999)

    assert result == 0
    mock_db_session.commit.assert_called_once()
