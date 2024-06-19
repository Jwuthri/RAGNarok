from typing import Literal, Optional
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel


class ModalitySchema(BaseModel):
    id: str = None
    modality: Literal["image", "video", "search", "answer", "slide"] = None
    prompt_id: Optional[str] = None

    meta: Optional[dict] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = str(uuid4)

    class Config:
        from_attributes = True
