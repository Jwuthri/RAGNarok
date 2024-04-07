from abc import ABC
from typing import Any

from pydantic import BaseModel


class ParserType(BaseModel):
    original_text: str
    parsed_text: Any


class ParserManager(ABC):
    @classmethod
    def parse(self, text: str, strict: bool = False) -> ParserType:
        ...
