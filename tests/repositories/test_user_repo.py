import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from datetime import datetime

from src.repositories.user import UserRepository
from src.db.user import UserTable
from src.schemas.user import UserSchema


@pytest.fixture
def mock_db_session():
    """Fixture to provide a mocked database session."""
    return create_autospec(Session, instance=True, spec_set=True)


@pytest.fixture
def user_data():
    """Provides a sample UserSchema data for testing."""
    return UserSchema(
        name="John Doe",
        email="john.doe@example.com",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def test_create_user(mock_db_session, user_data):
    """Test the create method of UserRepository."""
    repository = UserRepository(mock_db_session)
    returned_data = repository.create(user_data)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    assert returned_data == user_data, "The returned data should be the same as the input data."


def test_read_user_exists(mock_db_session, user_data):
    """Test reading an existing User record."""
    mock_db_session.query.return_value.filter.return_value.first.return_value = user_data

    repository = UserRepository(mock_db_session)
    result = repository.read(user_data.id)

    assert result == user_data, "The returned data should match the mock data."
    mock_db_session.query().filter().first.assert_called_once()


def test_read_user_not_exists(mock_db_session):
    """Test reading a User record that does not exist."""
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    repository = UserRepository(mock_db_session)
    result = repository.read(999)  # Assuming 999 does not exist

    assert result is None, "The result should be None for a non-existent record."


def test_update_user_exists(mock_db_session, user_data):
    """Test updating an existing User record."""
    updated_data = user_data.copy(update={"name": "Jane Doe"})
    mock_db_session.query.return_value.filter.return_value.first.return_value = updated_data

    repository = UserRepository(mock_db_session)
    result = repository.update(user_data.id, updated_data)

    assert result.name == "Jane Doe", "The name field should be updated."
    mock_db_session.commit.assert_called_once()


def test_delete_user_exists(mock_db_session):
    """Test deleting an existing User record."""
    mock_db_session.query.return_value.filter.return_value.delete.return_value = 1

    repository = UserRepository(mock_db_session)
    result = repository.delete(1)  # Assuming the user with ID 1 exists

    assert result == 1, "One record should be deleted."
    mock_db_session.commit.assert_called_once()


def test_delete_user_not_exists(mock_db_session):
    """Test attempting to delete a User record that does not exist."""
    mock_db_session.query.return_value.filter.return_value.delete.return_value = 0

    repository = UserRepository(mock_db_session)
    result = repository.delete(999)

    assert result == 0, "No record should be deleted."
    mock_db_session.commit.assert_called_once()
