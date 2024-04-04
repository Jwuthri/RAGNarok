from sqlalchemy import Column, func, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import Base


class IndexTable(Base):
    __tablename__ = "index_data"

    id = Column(String, primary_key=True)
    text = Column(String)
    meta = Column(JSONB, default={})
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
