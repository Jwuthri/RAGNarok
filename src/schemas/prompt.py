from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid5, NAMESPACE_DNS


class PromptSchema(BaseModel):
    id: UUID = None
    prompt: list[dict[str, str]]
    model_name: str
    latency: float
    cost: float
    prediction: str
    created_at: datetime = Field(default_factory=None)

    class Config:
        orm_mode = True
        from_attributes = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid5(NAMESPACE_DNS, f"{self.prompt}:{self.model_name}:{self.prediction}")
