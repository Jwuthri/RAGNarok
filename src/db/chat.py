from sqlalchemy import Column, func, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from src.migrations.env import Base


class ChatTable(Base):
    __tablename__ = "chat"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=True)
    thread_id = Column(String, nullable=True)
    assistant_id = Column(String, nullable=True)
    meta = Column(JSONB, nullable=True, default={})
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
