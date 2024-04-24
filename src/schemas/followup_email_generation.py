from datetime import datetime
from typing import Literal, Optional
from uuid import uuid5, NAMESPACE_DNS

from pydantic import BaseModel

from src.schemas.urn import URNSchema


class Hightlight(BaseModel):
    highlight: Optional[str] = None
    urn: Optional[URNSchema] = None
    urn_summary: Optional[str] = None
    question: str
    summary: str


class FollowUpEmailGenerationSchema(BaseModel):
    id: str = None
    org_id: str
    generated_email: Optional[str] = None
    highlights: list[Hightlight] = []
    prompt_id: Optional[str] = None

    creator_type: Literal["integration", "user", "simulation"] = None
    user_id: Optional[str] = None

    meta: Optional[dict] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.id = str(uuid5(NAMESPACE_DNS, f"{self.highlights}"))

    class Config:
        from_attributes = True
