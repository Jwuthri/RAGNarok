from abc import ABC, abstractmethod
from typing import Optional, Literal

from pydantic import BaseModel


class QueryTuneType(BaseModel):
    original_query: str
    refined_query: Optional[str] = None
    expanded_queries: Optional[list[str]] = None
    divided_queries: Optional[list[str]] = None
    func: Literal["expand", "refine", "divide"]
    cost: Optional[float] = None
    latency: Optional[float] = None


class QueryTuneManager(ABC):
    @abstractmethod
    def expand(self, query: str, n: Optional[int] = 3) -> QueryTuneType:
        ...

    @abstractmethod
    def refine(self, query: str) -> QueryTuneType:
        ...

    @abstractmethod
    def divide(self, query: str) -> QueryTuneType:
        ...

    @abstractmethod
    def describe_models(self):
        ...
