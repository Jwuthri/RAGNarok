import pytest
from unittest.mock import patch

from src.core.completion_parser._list import ListParser


@pytest.mark.parametrize(
    "input_text, expected_result",
    [
        ("[1, 2, 3]", [1, 2, 3]),
        ("['a', 'b', 'c']", ["a", "b", "c"]),
        ("[]", []),
        ("[{'key': 'value'}, {'another': 'item'}]", [{"key": "value"}, {"another": "item"}]),
    ],
)
def test_parse_valid_list(input_text, expected_result):
    result = ListParser.parse(input_text)
    assert result.original_completion == input_text
    assert result.parsed_completion == expected_result


@pytest.mark.parametrize("input_text", ["['unclosed list", "unenclosed text", "{not: 'a list'}", "12345"])
def test_parse_invalid_list(input_text):
    with patch("logging.Logger.error") as mock_logger_error:
        result = ListParser.parse(input_text)
        assert result.original_completion == input_text


def test_parse_empty_string():
    with patch("logging.Logger.error") as mock_logger_error:
        result = ListParser.parse("")
        assert result.original_completion == ""
        assert result.parsed_completion is None


def test_parse_non_list_structure():
    with patch("logging.Logger.error") as mock_logger_error:
        result = ListParser.parse("{'this': 'is a dictionary'}")
        assert result.original_completion == "{'this': 'is a dictionary'}"
        assert result.parsed_completion == {"this": "is a dictionary"}
