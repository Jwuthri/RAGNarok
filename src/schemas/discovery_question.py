from uuid import uuid5, NAMESPACE_DNS
from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class DiscoveryQuestionSchema(BaseModel):
    id: str = None
    org_id: str
    product_id: str

    question: str
    category: Optional[str] = None

    meta: Optional[dict] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_id()

    def set_id(self):
        self.id = str(uuid5(NAMESPACE_DNS, f"{self.org_id}:{self.product_id}:{self.question}"))

    class Config:
        from_attributes = True
