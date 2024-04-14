from sqlalchemy import Column, func, String, DateTime, ForeignKey, Boolean, text, BigInteger
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import Base


class BotTable(Base):
    __tablename__ = "bot"

    id = Column(String, primary_key=True)
    deal_id = Column(String, ForeignKey("deal.id"))
    org_id = Column(String, ForeignKey("org.id"))

    in_meeting = Column(Boolean, nullable=True)
    meeting_id = Column(String, nullable=True)
    meeting_url = Column(String, nullable=True)
    meeting_platform = Column(String, nullable=True)
    meeting_metadata = Column(JSONB, server_default=text("'{}'"), default={})
    meeting_participants = Column(JSONB, server_default=text("'{}'"), default={})

    join_at = Column(DateTime, server_default=func.now())
    status_changes = Column(JSONB, server_default=text("'{}'"), default={})
    participants = Column(JSONB, server_default=text("'[]'"), default=[])

    recording = Column(String, nullable=True)
    video_url = Column(String, nullable=True)
    s3_video_id = Column(String, server_default=None)

    meta = Column(JSONB, server_default=text("'{}'"), default={})
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class BotChatTable(Base):
    __tablename__ = "bot_chat"

    id = Column(BigInteger, primary_key=True)
    bot_id = Column(String, ForeignKey("bot.id"))
    to = Column(String, nullable=True)
    text = Column(String, nullable=True)
    sender = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class BotTranscriptionTable(Base):
    __tablename__ = "bot_transcription"

    id = Column(BigInteger, primary_key=True)
    bot_id = Column(String, ForeignKey("bot.id"))
    recording_id = Column(String, nullable=True)
    transcript = Column(JSONB, server_default=text("'{}'"), default={})
    created_at = Column(DateTime, server_default=func.now())


class BotStatusTable(Base):
    __tablename__ = "bot_status"

    id = Column(BigInteger, primary_key=True)
    bot_id = Column(String, ForeignKey("bot.id"))
    code_status = Column(String, nullable=True)
    sub_code = Column(String, nullable=True)
    message = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class BotParticipantsTable(Base):
    __tablename__ = "bot_participants"

    id = Column(String, primary_key=True)
    bot_id = Column(String, ForeignKey("bot.id"))
    name = Column(String)
    employee = Column(Boolean)
    email = Column(String, nullable=True)

    meta = Column(JSONB, server_default=text("'{}'"), default={})
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
