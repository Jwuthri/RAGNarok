from uuid import uuid5, NAMESPACE_DNS
from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class DealDiscoveryQuestion(BaseModel):
    id: str = None
    deal_id: str
    org_id: str
    discovery_question_id: str
    product_id: str = None
    prompt_id: Optional[str] = None

    category: Optional[str] = None
    answer: Optional[str] = None

    meta: Optional[dict] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_id()

    def set_id(self):
        self.id = str(
            uuid5(NAMESPACE_DNS, f"{self.org_id}:{self.deal_id}:{self.product_id}:{self.discovery_question_id}")
        )

    class Config:
        from_attributes = True
