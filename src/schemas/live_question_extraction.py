from datetime import datetime
from typing import Optional, Any
from uuid import uuid5, NAMESPACE_DNS

from pydantic import BaseModel


class LiveQuestionExtractionSchema(BaseModel):
    id: str = None
    bot_id: str
    deal_id: str
    org_id: str
    seconds_ago: Optional[int] = None
    question_extracted: Optional[str] = None
    confidence: Optional[int] = 0

    meta: Optional[dict] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.id = str(uuid5(NAMESPACE_DNS, f"{self.org_id}:{self.bot_id}:{self.deal_id}"))

    class Config:
        from_attributes = True
