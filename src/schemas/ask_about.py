from uuid import uuid4
from typing import Literal, Optional
from datetime import datetime

from pydantic import BaseModel

from src.schemas.urn import URNSchema


class AskAboutSchema(BaseModel):
    id: str = None
    chat_id: Optional[str] = None
    prompt_id: Optional[str] = None

    org_id: str
    user_id: str
    creator_type: str
    deal_id: Optional[str] = None
    org_name: Optional[str] = None
    deal_name: Optional[str] = None
    product_id: Optional[str] = None
    product_name: Optional[str] = None

    question: str
    answer: Optional[str] = None
    summary: Optional[str] = None
    follow_up: Optional[str] = None
    inscope: Optional[bool] = None
    intent: Optional[str] = None
    modality: Optional[str] = None

    qa_type: Literal["product", "deal"]
    source_urns: Optional[list[URNSchema]] = None
    video_urn: Optional[URNSchema] = None
    image_urn: Optional[URNSchema] = None

    roadmap: Optional[list[dict]] = None
    fuds: Optional[list[dict]] = None
    knowledge_data: Optional[list[dict]] = []
    answered_from_cache: Optional[bool] = False

    meta: Optional[dict] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = str(uuid4())

    class Config:
        from_attributes = True
