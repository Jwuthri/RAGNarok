from datetime import datetime
from typing import Literal, Optional
from uuid import uuid5, NAMESPACE_DNS

from pydantic import BaseModel


class ChatMessage(BaseModel):
    id: str = None
    message: str
    role: Literal["system", "user", "assistant"]

    meta: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = str(uuid5(NAMESPACE_DNS, f"{self.role}:{self.message}:{self.created_at}"))

    class Config:
        from_attributes = True
