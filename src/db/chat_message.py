from sqlalchemy import Column, func, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from src.migrations.env import Base


class ChatMessageTable(Base):
    __tablename__ = "chat_message"

    id = Column(String, primary_key=True)
    role = Column(str)
    message = Column(str)
    meta = Column(JSONB, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
