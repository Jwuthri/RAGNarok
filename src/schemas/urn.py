from typing import Optional
from pydantic import BaseModel


class URN(BaseModel):
    type: str
    id: str
    name: Optional[str] = None
    url: Optional[str] = None
