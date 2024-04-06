from typing import Optional
from datetime import datetime
from uuid import uuid5, NAMESPACE_DNS

from pydantic import BaseModel


class ChatHistorySchema(BaseModel):
    id: str = None
    chat_message_id: str
    meta: Optional[dict] = None
    chat_id: Optional[str] = None
    prompt_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = str(uuid5(NAMESPACE_DNS, f"{self.chat_id}:{self.chat_message_id}:{self.created_at}"))

    class Config:
        from_attributes = True
