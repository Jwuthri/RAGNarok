import logging
import json

from src.core.completion_parser.base import ParserManager, ParserType

logger = logging.getLogger(__name__)


class JsonParser(ParserManager):
    @classmethod
    def parse(self, text: str, strict: bool = False) -> ParserType:
        def attempt_parse(json_str: str) -> dict | None:
            try:
                return json.loads(json_str, strict=strict)
            except json.JSONDecodeError as e:
                logger.error(f"Can't JsonParser.parse for {text}", extra={"error": e})
                return None

        parsed_text = attempt_parse(text)
        if parsed_text:
            return ParserType(original_completion=text, parsed_completion=parsed_text)

        new_s, stack, is_inside_string, escaped = "", [], False, False
        for char in text:
            if is_inside_string:
                if char == '"' and not escaped:
                    is_inside_string = False
                elif char == "\\":
                    escaped = not escaped
                else:
                    escaped = False
                    if char == "\n":
                        char = "\\n"
            else:
                if char == '"':
                    is_inside_string = True
                elif char in "{[":
                    stack.append("}" if char == "{" else "]")
                elif char in "}]" and stack and char == stack[-1]:
                    stack.pop()
                else:
                    continue
            new_s += char
        new_s += "".join(reversed(stack))

        return ParserType(original_completion=text, parsed_completion=attempt_parse(new_s) or attempt_parse(text))


if __name__ == "__main__":
    print(JsonParser.parse("idk"))
