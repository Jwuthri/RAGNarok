from uuid import uuid5, NAMESPACE_DNS
from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class DealKnowledgeExtractionSchema(BaseModel):
    id: str = None
    bot_id: str
    deal_id: str
    org_id: str
    seconds_ago: Optional[int] = None
    prompt_id: Optional[str] = None
    meeting_timestamp: Optional[float] = None
    knowledge: Optional[dict] = None
    knowledge_text: Optional[str] = None

    meta: Optional[dict] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_id()

    def set_id(self):
        self.id = str(uuid5(NAMESPACE_DNS, f"{self.org_id}:{self.deal_id}:{self.knowledge_text}"))

    class Config:
        from_attributes = True

    def model_dump(self) -> dict:
        data = {
            "id": self.id,
            "bot_id": self.bot_id,
            "deal_id": self.deal_id,
            "org_id": self.org_id,
            "prompt_id": self.prompt_id,
            "meeting_timestamp": self.meeting_timestamp,
            "knowledge": self.knowledge,
            "knowledge_text": self.knowledge_text,
            "meta": self.meta,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

        return data
