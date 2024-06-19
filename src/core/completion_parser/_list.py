import logging
import ast

from src.core.completion_parser.base import ParserManager, ParserType

logger = logging.getLogger(__name__)


class ListParser(ParserManager):
    @classmethod
    def parse(self, text: str, strict: bool = False) -> ParserType:
        parsed_completion = None
        try:
            parsed_completion = ast.literal_eval(text)
        except Exception as e:
            logger.error(f"Can't parse_list for {text}", extra={"error": e})

        return ParserType(original_completion=text, parsed_completion=parsed_completion)


if __name__ == "__main__":
    print(ListParser.parse("[{'toto': 1}]"))
