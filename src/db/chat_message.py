from sqlalchemy import Column, ForeignKey, func, String, DateTime, text
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import Base


class ChatMessageTable(Base):
    __tablename__ = "chat_message"

    id = Column(String, primary_key=True)
    chat_id = Column(String, ForeignKey("chat.id"), nullable=False)
    prompt_id = Column(String, ForeignKey("prompt.id"), nullable=False)
    role = Column(String)
    message = Column(String)

    meta = Column(JSONB, server_default=text("'{}'"), default={})
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
