from typing import Optional
from datetime import datetime
from uuid import uuid5, NAMESPACE_DNS

from pydantic import BaseModel


class ChatSchema(BaseModel):
    id: str = None
    chat_type: Optional[str] = None
    user_id: Optional[str] = None
    bot_id: Optional[str] = None
    deal_id: Optional[str] = None
    org_id: Optional[str] = None
    thread_id: Optional[str] = None
    assistant_id: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    meta: Optional[dict] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = str(
            uuid5(
                NAMESPACE_DNS,
                f"{self.user_id}:{self.thread_id}:{self.meta}:{self.bot_id}:{self.chat_type}:{self.deal_id}:{self.org_id}",
            )
        )

    class Config:
        from_attributes = True
