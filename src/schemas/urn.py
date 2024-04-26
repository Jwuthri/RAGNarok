from typing import Optional
from pydantic import BaseModel


class URNSchema(BaseModel):
    type: str
    id: str
    name: Optional[str] = None
    url: Optional[str] = None
    score: Optional[float] = None
    timestamp: Optional[float] = None
