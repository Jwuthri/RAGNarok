import pytest
from datetime import datetime
from uuid import uuid5, NAMESPACE_DNS

from src.schemas.index import IndexSchema


def test_index_schema_id_generation():
    text = "Example text"
    meta = {"key": "value"}

    index = IndexSchema(text=text, meta=meta)

    expected_id = str(uuid5(NAMESPACE_DNS, f"{text}:{meta}"))
    assert index.id == expected_id, "The ID should be generated based on text and meta."


def test_index_schema_mandatory_fields():
    text = "Mandatory text"
    meta = {"mandatory": "info"}

    index = IndexSchema(text=text, meta=meta)

    assert index.text == text, "Text should be correctly assigned."
    assert index.meta == meta, "Meta should be correctly assigned."


def test_index_schema_optional_fields():
    now = datetime.now()
    text = "Optional Fields Test"
    meta = {"optional": "field test"}

    index = IndexSchema(text=text, meta=meta, created_at=now, updated_at=now)

    assert index.created_at == now, "created_at should match the provided datetime."
    assert index.updated_at == now, "updated_at should match the provided datetime."


@pytest.mark.parametrize("meta", [{}, {"example": "data"}])
def test_index_schema_with_various_meta(meta):
    text = "Testing various meta"

    index = IndexSchema(text=text, meta=meta)

    assert index.meta == meta, "Meta should be correctly assigned regardless of its content."
