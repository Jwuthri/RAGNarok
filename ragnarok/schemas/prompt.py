from typing import Optional, Any
from datetime import datetime
from uuid import uuid5, NAMESPACE_DNS

from pydantic import BaseModel


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
    tools_call: Optional[list[ToolCall]] = {}
    prompt_tokens: int
    completion_tokens: int
    prompt: list[dict] = []

    meta: Optional[dict] = {}
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

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
            "tools_call": self.tools_call.model_dump() if self.tools_call else {},
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "prompt": [{"role": x.get("role"), "content": x.get("message")} for x in self.prompt]
            if self.prompt
            else {},
            "meta": self.meta,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

        return data
