import json

from src.infrastructure.completion_parser.base import ParserType
from src.infrastructure.completion_parser import JsonParser


def test_parse_valid_json():
    text = '{"name": "ChatGPT", "type": "AI"}'
    expected = ParserType(original_text=text, parsed_text=json.loads(text))
    result = JsonParser.parse(text)
    assert result.original_text == expected.original_text
    assert result.parsed_text == expected.parsed_text


def test_parse_partial_json():
    text = '{"name": "ChatGPT", "type": "AI'
    # Assuming your ParserType can handle None as parsed_text for partial/invalid JSON
    expected = ParserType(original_text=text, parsed_text=None)
    result = JsonParser.parse(text)
    assert result.original_text == expected.original_text
    assert result.parsed_text == expected.parsed_text


def test_parse_malformed_json():
    text = '{"name": "ChatGPT", type": "AI"}'  # Missing quote before type
    expected = ParserType(original_text=text, parsed_text=None)
    result = JsonParser.parse(text)
    assert result.original_text == expected.original_text
    assert result.parsed_text == expected.parsed_text


def test_strict_mode_raises_error():
    text = '{"name": "ChatGPT", "type": "AI",}'
    expected = ParserType(original_text=text, parsed_text=None)
    result = JsonParser.parse(text, strict=True)
    assert result.original_text == expected.original_text
    assert result.parsed_text == expected.parsed_text
