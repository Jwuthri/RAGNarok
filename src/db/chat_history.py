from sqlalchemy import Column, ForeignKey, func, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import Base


class ChatHistoryTable(Base):
    __tablename__ = "chat_history"

    id = Column(String, primary_key=True)
    chat_message = Column(JSONB)
    meta = Column(JSONB, nullable=True, default={})
    prompt_id = Column(String, ForeignKey("prompt.id"))
    created_at = Column(DateTime, server_default=func.now())
    chat_id = Column(String, ForeignKey("chat.id"), primary_key=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
