import pytest
from datetime import datetime
from uuid import uuid5, NAMESPACE_DNS

from src.schemas.user import UserSchema


def test_user_schema_id_generation():
    name = "John Doe"
    email = "johndoe@example.com"

    user = UserSchema(name=name, email=email)

    expected_id = str(uuid5(NAMESPACE_DNS, f"{name}:{email}"))
    assert user.id == expected_id, "The ID should be generated based on name and email."


def test_user_schema_optional_fields():
    name = "Jane Doe"
    email = "janedoe@example.com"

    user = UserSchema(name=name, email=email)

    assert user.meta == {}, "Meta should be None by default."
    assert user.created_at is None, "created_at should be None by default."
    assert user.updated_at is None, "updated_at should be None by default."


def test_user_schema_with_timestamps():
    now = datetime.now()
    name = "Jim Beam"
    email = "jimbeam@example.com"

    user = UserSchema(name=name, email=email, created_at=now, updated_at=now)

    assert user.created_at == now, "created_at should match the provided datetime."
    assert user.updated_at == now, "updated_at should match the provided datetime."


@pytest.mark.parametrize("meta", [{}, {"role": "admin"}])
def test_user_schema_with_meta(meta):
    name = "Jack Daniels"
    email = "jackdaniels@example.com"

    user = UserSchema(name=name, email=email, meta=meta)

    assert user.meta == meta, "Meta should be correctly assigned."
