from datetime import datetime
from typing import Optional, Any
from uuid import uuid5, NAMESPACE_DNS

from pydantic import BaseModel


class Product(BaseModel):
    id: str = None
    name: str
    default: bool
    org_name: str

    meta: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.id = str(uuid5(NAMESPACE_DNS, f"{self.org_name}:{self.name}"))

    class Config:
        from_attributes = True
