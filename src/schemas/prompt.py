from typing import Optional, Any
from datetime import datetime
from uuid import uuid5, NAMESPACE_DNS

from pydantic import BaseModel

from src.schemas.chat_message import ChatMessageSchema


class ToolCall(BaseModel):
    id: str
    function: dict[str, Any]
    type: str


class PromptSchema(BaseModel):
    id: str = None
    cost: float
    latency: float
    llm_name: str
    prediction: Optional[str] = None
    tool_call: Optional[ToolCall] = {}
    prompt_tokens: int
    completion_tokens: int
    prompt: list[ChatMessageSchema]
    meta: Optional[dict] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = str(str(uuid5(NAMESPACE_DNS, f"{self.prompt}:{self.llm_name}:{self.prediction}")))

    class Config:
        from_attributes = True

    def model_dump(self) -> dict:
        data = {
            "id": self.id,
            "cost": self.cost,
            "latency": self.latency,
            "llm_name": self.llm_name,
            "prediction": self.prediction,
            "tool_call": self.tool_call.model_dump() if self.tool_call else {},
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "prompt": [{"role": x.role, "content": x.message} for x in self.prompt] if self.prompt else {},
            "meta": self.meta,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

        return data
