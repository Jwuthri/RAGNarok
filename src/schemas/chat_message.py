from datetime import datetime
from typing import Literal, Optional
from uuid import UUID, uuid5, NAMESPACE_DNS

from pydantic import BaseModel


class ChatMessage(BaseModel):
    id: str = None
    message: str
    meta: Optional[dict] = None
    created_at: Optional[datetime] = None
    role: Literal["system", "user", "assistant"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = str(uuid5(NAMESPACE_DNS, f"{self.role}:{self.message}:{self.created_at}"))

    class Config:
        orm_mode = True
        from_attributes = True
