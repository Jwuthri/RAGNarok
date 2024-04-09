from datetime import datetime
from typing import Optional, Any
from uuid import uuid5, NAMESPACE_DNS

from pydantic import BaseModel


class ChatHistorySchema(BaseModel):
    id: str
    deal_id: str
    org_id: str

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


class BotTranscription(BaseModel):
    bot_id: str
    recording_id: str
    transcript: dict[str, Any]
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BotStatus(BaseModel):
    bot_id: str
    code_status: str
    sub_code: Optional[str] = None
    message: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BotChat(BaseModel):
    bot_id: str
    to: str
    text: str
    sender: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BotParticipants(BaseModel):
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
