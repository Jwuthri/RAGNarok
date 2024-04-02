from pydantic import BaseModel
from datetime import datetime, timezone
from uuid import UUID, uuid5, NAMESPACE_DNS


class PromptSchema(BaseModel):
    id: UUID = None
    prompt: list[dict[str, str]]
    model_name: str
    latency: float
    cost: float
    prediction: str
    prompt_tokens: int
    completion_tokens: int
    created_at: datetime = datetime.now(timezone.utc)
    meta: dict = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid5(NAMESPACE_DNS, f"{self.prompt}:{self.model_name}:{self.prediction}")

    class Config:
        orm_mode = True
        from_attributes = True
