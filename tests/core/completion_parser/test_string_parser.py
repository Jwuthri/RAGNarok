from src.core.completion_parser.base import ParserType
from src.core.completion_parser import StringParser


def test_parse_simple_string():
    text = "Hello, world!"
    expected = ParserType(original_completion=text, parsed_completion=text)
    result = StringParser.parse(text)
    assert result.original_completion == expected.original_completion
    assert result.parsed_completion == expected.parsed_completion


def test_parse_empty_string():
    text = ""
    expected = ParserType(original_completion=text, parsed_completion=text)
    result = StringParser.parse(text)
    assert result.original_completion == expected.original_completion
    assert result.parsed_completion == expected.parsed_completion


def test_parse_complex_string():
    text = '{"name": "ChatGPT", "type": "AI"}'  # This is a string, not JSON in this context
    expected = ParserType(original_completion=text, parsed_completion=text)
    result = StringParser.parse(text)
    assert result.original_completion == expected.original_completion
    assert result.parsed_completion == expected.parsed_completion


def test_parse_string_with_newlines():
    text = "Hello,\nworld!"
    expected = ParserType(original_completion=text, parsed_completion=text)
    result = StringParser.parse(text)
    assert result.original_completion == expected.original_completion
    assert result.parsed_completion == expected.parsed_completion
