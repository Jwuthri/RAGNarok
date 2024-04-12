from datetime import datetime
from typing import Optional, Any
from uuid import uuid5, NAMESPACE_DNS

from pydantic import BaseModel


class LiveQuestionSchema(BaseModel):
    id: str = None
    bot_id: str
    deal_id: str
    org_name: str
    seconds_ago: Optional[int] = None

    meta: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.id = str(uuid5(NAMESPACE_DNS, f"{self.org_name}:{self.bot_id}:{self.deal_id}"))

    class Config:
        from_attributes = True
