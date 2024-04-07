from src.infrastructure.completion_parser.base import ParserType
from src.infrastructure.completion_parser import StringParser


def test_parse_simple_string():
    text = "Hello, world!"
    expected = ParserType(original_text=text, parsed_text=text)
    result = StringParser.parse(text)
    assert result.original_text == expected.original_text
    assert result.parsed_text == expected.parsed_text


def test_parse_empty_string():
    text = ""
    expected = ParserType(original_text=text, parsed_text=text)
    result = StringParser.parse(text)
    assert result.original_text == expected.original_text
    assert result.parsed_text == expected.parsed_text


def test_parse_complex_string():
    text = '{"name": "ChatGPT", "type": "AI"}'  # This is a string, not JSON in this context
    expected = ParserType(original_text=text, parsed_text=text)
    result = StringParser.parse(text)
    assert result.original_text == expected.original_text
    assert result.parsed_text == expected.parsed_text


def test_parse_string_with_newlines():
    text = "Hello,\nworld!"
    expected = ParserType(original_text=text, parsed_text=text)
    result = StringParser.parse(text)
    assert result.original_text == expected.original_text
    assert result.parsed_text == expected.parsed_text
