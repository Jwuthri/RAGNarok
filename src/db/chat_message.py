from sqlalchemy import Column, func, String, DateTime, text
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import Base


class ChatMessageTable(Base):
    __tablename__ = "chat_message"

    id = Column(String, primary_key=True)
    role = Column(String)
    message = Column(String)

    meta = Column(JSONB, nullable=True, server_default=text("'{}'"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
