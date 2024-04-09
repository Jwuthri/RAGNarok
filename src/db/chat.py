from sqlalchemy import Column, func, String, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import Base


class ChatTable(Base):
    __tablename__ = "chat"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=True)
    bot_id = Column(String, ForeignKey("bot.id"), nullable=True)
    chat_type = Column(String, nullable=True)
    thread_id = Column(String, nullable=True)
    assistant_id = Column(String, nullable=True)

    meta = Column(JSONB, nullable=True, server_default=text("'{}'"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
