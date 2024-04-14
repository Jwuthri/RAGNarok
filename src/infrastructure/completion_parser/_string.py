import logging

from src.infrastructure.completion_parser.base import ParserManager, ParserType

logger = logging.getLogger(__name__)


class StringParser(ParserManager):
    @classmethod
    def parse(self, text: str, strict: bool = False) -> ParserType:
        return ParserType(original_text=text, parsed_text=text)


if __name__ == "__main__":
    print(StringParser.parse("idk"))
