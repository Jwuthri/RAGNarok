from datetime import datetime
from typing import Literal, Optional
from uuid import uuid5, NAMESPACE_DNS

from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: str = None
    name: str
    default: bool
    org_id: str
    creator_type: Literal["integration", "user", "simulation"] = None

    meta: Optional[dict] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.id = str(uuid5(NAMESPACE_DNS, f"{self.org_id}:{self.name}"))

    class Config:
        from_attributes = True
