from datetime import datetime
from typing import Optional
from uuid import uuid5, NAMESPACE_DNS

from pydantic import BaseModel


class BotSchema(BaseModel):
    id: str
    deal_id: str
    org_name: str

    in_meeting: bool = False
    meeting_id: Optional[str] = None
    meeting_url: Optional[str] = None
    meeting_platform: Optional[str] = None
    meeting_participants: Optional[list[str]] = None
    meeting_metadata: Optional[dict] = None

    participants: Optional[list[str]] = []
    status_changes: Optional[list] = None
    join_at: Optional[datetime] = None
    s3_video_id: Optional[str] = None
    recording: Optional[str] = None
    video_url: Optional[str] = None

    meta: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BotTranscriptionSchema(BaseModel):
    bot_id: str
    text: str
    end_time: float
    recording_id: str
    start_time: float
    speaker: Optional[str] = None
    language: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BotStatusSchema(BaseModel):
    bot_id: str
    code_status: str
    sub_code: Optional[str] = None
    message: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BotChatSchema(BaseModel):
    bot_id: str
    to: str
    text: str
    sender: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BotParticipantsSchema(BaseModel):
    id: str = None
    bot_id: str
    name: str
    email: Optional[str] = None
    employee: Optional[bool] = False

    meta: Optional[dict] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.id = str(uuid5(NAMESPACE_DNS, f"{self.bot_id}:{self.name}"))

    class Config:
        from_attributes = True
