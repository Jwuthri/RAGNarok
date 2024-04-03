from sqlalchemy import Column, func, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from src.migrations.env import Base


class ChatMessageTable(Base):
    __tablename__ = "chat_message"

    id = Column(String, primary_key=True)
    role = Column(String)
    message = Column(String)
    meta = Column(JSONB, nullable=True, default={})
    created_at = Column(DateTime, server_default=func.now())
