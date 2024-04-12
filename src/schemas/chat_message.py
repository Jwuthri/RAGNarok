from datetime import datetime
from typing import Literal, Optional
from uuid import uuid5, NAMESPACE_DNS, uuid4

from pydantic import BaseModel


class ChatMessageSchema(BaseModel):
    id: str = None
    message: str
    chat_id: str
    prompt_id: Optional[str] = None
    role: Literal["system", "user", "assistant"]

    meta: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = str(uuid4())

    class Config:
        from_attributes = True
