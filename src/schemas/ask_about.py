from uuid import uuid4
from typing import Literal, Optional
from datetime import datetime

from pydantic import BaseModel

from src.schemas.urn import URNSchema


class AskAboutSchema(BaseModel):
    id: str = None
    chat_id: str
    prompt_ids: Optional[list[str]] = None

    org_id: str
    org_name: str
    user_id: str
    user_type: str
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    deal_id: Optional[str] = None
    deal_name: Optional[str] = None

    answer: str
    answer_blob: dict
    summary: str
    follow_up: str
    confidence: int
    inscope: bool
    intent: str

    latency: float
    cost: float
    qa_type: Literal["product", "deal"]
    source_urns: list[URNSchema]
    video_urn: Optional[URNSchema] = None
    image_urn: Optional[URNSchema] = None

    roadmap: Optional[list[dict]] = None
    fuds: Optional[list[dict]] = None
    knowledge_data: Optional[list[dict]] = []

    answered_from_cache: bool
    use_cache: bool

    meta: Optional[dict] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = str(uuid4())

    class Config:
        from_attributes = True
