from sqlalchemy import Column, ForeignKey, func, String, DateTime, text
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import Base


class DiscoveryQuestion(Base):
    __tablename__ = "discovery_question"

    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("org.id"))
    product_id = Column(String, ForeignKey("product.id"))

    category = Column(String, nullable=True)
    question = Column(String)

    meta = Column(JSONB, server_default=text("'{}'"), default={})
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
