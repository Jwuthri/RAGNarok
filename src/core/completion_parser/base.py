from abc import ABC
from typing import Any

from pydantic import BaseModel


class ParserType(BaseModel):
    original_completion: str
    parsed_completion: Any


class ParserManager(ABC):
    @classmethod
    def parse(self, text: str, strict: bool = False) -> ParserType:
        ...
