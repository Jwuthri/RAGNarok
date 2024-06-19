from typing import Optional
from pydantic import BaseModel


class URNSchema(BaseModel):
    id: str
    type: str
    url: Optional[str] = None
    name: Optional[str] = None
    score: Optional[float] = None
    timestamp: Optional[float] = None

    class Config:
        from_attributes = True
