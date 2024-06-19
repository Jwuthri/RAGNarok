import logging

from ragnarok.core.completion_parser.base import ParserManager, ParserType

logger = logging.getLogger(__name__)


class StringParser(ParserManager):
    @classmethod
    def parse(self, text: str, strict: bool = False) -> ParserType:
        return ParserType(original_completion=text, parsed_completion=text)


if __name__ == "__main__":
    print(StringParser.parse("idk"))
