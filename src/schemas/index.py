from typing import Optional
from datetime import datetime
from uuid import UUID, uuid5, NAMESPACE_DNS

from pydantic import BaseModel


class IndexSchema(BaseModel):
    id: str = None
    text: str
    meta: dict
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = str(uuid5(NAMESPACE_DNS, f"{self.text}:{self.meta}"))

    class Config:
        from_attributes = True
