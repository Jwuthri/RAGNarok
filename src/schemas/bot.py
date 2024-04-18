from datetime import datetime
from typing import Optional
from uuid import uuid5, NAMESPACE_DNS, uuid4

from pydantic import BaseModel


class BotSchema(BaseModel):
    id: str
    org_id: str
    deal_id: str

    in_meeting: bool = False
    meeting_id: Optional[str] = None
    meeting_url: Optional[str] = None
    meeting_platform: Optional[str] = None
    meeting_metadata: Optional[dict] = {}
    meeting_participants: Optional[list[str]] = []

    status_changes: Optional[list[dict]] = []
    participants: Optional[list[str]] = []
    join_at: Optional[datetime] = None
    s3_video_id: Optional[str] = None
    recording: Optional[str] = None
    video_url: Optional[str] = None

    meta: Optional[dict] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BotTranscriptionSchema(BaseModel):
    id: str = None
    text: str
    bot_id: str
    end_time: float
    start_time: float
    recording_id: Optional[str] = None
    speaker: Optional[str] = None
    language: Optional[str] = None
    is_final: Optional[bool] = True
    created_at: Optional[datetime] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.id = str(uuid4)

    class Config:
        from_attributes = True


class BotStatusSchema(BaseModel):
    id: str = None
    bot_id: str
    code_status: str
    message: Optional[str] = None
    sub_code: Optional[str] = None
    created_at: Optional[datetime] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.id = str(uuid4)

    class Config:
        from_attributes = True


class BotChatSchema(BaseModel):
    id: str = None
    to: str
    text: str
    bot_id: str
    sender: str
    created_at: Optional[datetime] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.id = str(uuid4)

    class Config:
        from_attributes = True


class BotParticipantsSchema(BaseModel):
    id: str = None
    bot_id: str
    name: str
    email: Optional[str] = None
    employee: Optional[bool] = False

    meta: Optional[dict] = {}
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.id = str(uuid5(NAMESPACE_DNS, f"{self.bot_id}:{self.name}"))

    class Config:
        from_attributes = True
