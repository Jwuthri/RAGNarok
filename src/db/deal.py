from sqlalchemy import Column, func, String, DateTime, ForeignKey, Boolean, text, BigInteger
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import Base


class Deal(Base):
    __tablename__ = "deal"

    id = Column(String, primary_key=True)
    name = Column(String)
    status = Column(String)
    org_name = Column(String)

    owner = Column(String, nullable=True)
    email_domain = Column(String, nullable=True)
    contacts = Column(JSONB, nullable=True)
    creator_type = Column(String, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    meta = Column(JSONB, server_default=text("'{}'"))
