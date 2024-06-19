import json

from ragnarok.core.completion_parser.base import ParserType
from ragnarok.core.completion_parser import JsonParser


def test_parse_valid_json():
    text = '{"name": "ChatGPT", "type": "AI"}'
    expected = ParserType(original_completion=text, parsed_completion=json.loads(text))
    result = JsonParser.parse(text)
    assert result.original_completion == expected.original_completion
    assert result.parsed_completion == expected.parsed_completion


def test_parse_partial_json():
    text = '{"name": "ChatGPT", "type": "AI'
    # Assuming your ParserType can handle None as parsed_text for partial/invalid JSON
    expected = ParserType(original_completion=text, parsed_completion=None)
    result = JsonParser.parse(text)
    assert result.original_completion == expected.original_completion
    assert result.parsed_completion == expected.parsed_completion


def test_parse_malformed_json():
    text = '{"name": "ChatGPT", type": "AI"}'  # Missing quote before type
    expected = ParserType(original_completion=text, parsed_completion=None)
    result = JsonParser.parse(text)
    assert result.original_completion == expected.original_completion
    assert result.parsed_completion == expected.parsed_completion


def test_strict_mode_raises_error():
    text = '{"name": "ChatGPT", "type": "AI",}'
    expected = ParserType(original_completion=text, parsed_completion=None)
    result = JsonParser.parse(text, strict=True)
    assert result.original_completion == expected.original_completion
    assert result.parsed_completion == expected.parsed_completion
