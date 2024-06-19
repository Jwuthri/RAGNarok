from uuid import uuid4
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class ChatMessageSchema(BaseModel):
    id: str = None
    message: str
    chat_id: Optional[str] = None
    prompt_id: Optional[str] = None
    role: Literal["system", "user", "assistant"]

    meta: Optional[dict] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = str(uuid4())

    class Config:
        from_attributes = True

    def model_dump(self) -> dict:
        return {
            "id": self.id,
            "message": self.message,
            "chat_id": self.chat_id,
            "prompt_id": self.prompt_id,
            "role": self.role,
            "meta": self.meta,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None,
        }
