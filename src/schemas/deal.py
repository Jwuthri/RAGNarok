from datetime import datetime
from typing import Optional, Literal
from uuid import uuid5, NAMESPACE_DNS

from pydantic import BaseModel


class DealSchema(BaseModel):
    id: str = None
    name: str
    status: Literal["active", "inactive"] = None
    org_name: str

    owner: Optional[str] = None
    email_domain: Optional[str] = None
    contacts: Optional[list[str]] = None

    creator_type: Literal["integration", "user", "simulation"] = None

    meta: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.id = str(uuid5(NAMESPACE_DNS, f"{self.org_name}:{self.name}"))

    class Config:
        from_attributes = True
