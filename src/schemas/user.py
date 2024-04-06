from typing import Optional
from datetime import datetime
from uuid import uuid5, NAMESPACE_DNS

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: str = None
    name: str
    email: str
    meta: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = str(uuid5(NAMESPACE_DNS, f"{self.name}:{self.email}"))

    class Config:
        from_attributes = True
