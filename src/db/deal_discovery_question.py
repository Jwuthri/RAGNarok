from sqlalchemy import Column, ForeignKey, func, String, DateTime, text
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import Base


class DealDiscoveryQuestion(Base):
    __tablename__ = "deal_discovery_question"

    id = Column(String, primary_key=True)
    chat_id = Column(String, ForeignKey("chat.id"))
    prompt_id = Column(String, ForeignKey("prompt.id"), nullable=True)
    deal_id = Column(String, ForeignKey("deal.id"))
    org_id = Column(String, ForeignKey("org.id"))
    discovery_question_id = Column(String, ForeignKey("discovery_question.id"))
    product_id = Column(String, ForeignKey("product.id"))

    category = Column(String, nullable=True)
    answer = Column(String)

    meta = Column(JSONB, server_default=text("'{}'"), default={})
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    updated_by = Column(String, nullable=True)
