from sqlalchemy import Column, func, String, DateTime, text
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import Base


class OrgTable(Base):
    __tablename__ = "org"

    id = Column(String, primary_key=True)
    name = Column(String)
    status = Column(String)
    creator_type = Column(String)

    meta = Column(JSONB, server_default=text("'{}'"), default={})
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
