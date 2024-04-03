from typing import Optional
from datetime import datetime
from uuid import UUID, uuid5, NAMESPACE_DNS

from pydantic import BaseModel

from src.schemas.chat_message import ChatMessage


class PromptSchema(BaseModel):
    id: str = None
    cost: float
    latency: float
    model_name: str
    prediction: str
    prompt_tokens: int
    completion_tokens: int
    prompt: list[ChatMessage]
    meta: Optional[dict] = None
    created_at: Optional[datetime] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = str(str(uuid5(NAMESPACE_DNS, f"{self.prompt}:{self.model_name}:{self.prediction}")))

    class Config:
        orm_mode = True
        from_attributes = True
