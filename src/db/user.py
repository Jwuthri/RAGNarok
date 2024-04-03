from sqlalchemy import Column, func, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from src.migrations.env import Base


class UserTable(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    meta = Column(JSONB, nullable=True, default={})
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
