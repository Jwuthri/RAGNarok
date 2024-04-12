from sqlalchemy import Column, func, String, DateTime, ForeignKey, Boolean, text, BigInteger
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import Base


class ProductTable(Base):
    __tablename__ = "product"

    id = Column(String, primary_key=True)
    name = Column(String)
    org_name = Column(String)
    default = Column(Boolean, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    meta = Column(JSONB, server_default=text("'{}'"))
