from typing import Optional
from datetime import datetime
from uuid import UUID, uuid5, NAMESPACE_DNS

from pydantic import BaseModel

from src.schemas.chat_message import ChatMessage


class ChatHistorySchema(BaseModel):
    id: str = None
    chat_message: ChatMessage
    meta: Optional[dict] = None
    chat_id: Optional[str] = None
    prompt_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = str(uuid5(NAMESPACE_DNS, f"{self.chat_id}:{self.chat_message}:{self.created_at}"))

    class Config:
        from_attributes = True
