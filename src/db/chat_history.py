from sqlalchemy import Column, ForeignKey, func, String, DateTime, text
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import Base


class ChatHistoryTable(Base):
    __tablename__ = "chat_history"

    id = Column(String, primary_key=True)
    prompt_id = Column(String, ForeignKey("prompt.id"))
    created_at = Column(DateTime, server_default=func.now())
    chat_message_id = Column(String, ForeignKey("chat_message.id"))
    chat_id = Column(String, ForeignKey("chat.id"), primary_key=True)

    meta = Column(JSONB, nullable=True, server_default=text("'{}'"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
