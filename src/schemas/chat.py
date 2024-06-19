from typing import Optional
from datetime import datetime
from uuid import uuid5, NAMESPACE_DNS

from pydantic import BaseModel


class ChatSchema(BaseModel):
    id: str = None
    chat_type: Optional[str] = None
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
                f"{self.thread_id}:{self.meta}:{self.chat_type}",
            )
        )

    class Config:
        from_attributes = True
