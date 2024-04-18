from sqlalchemy import Column, ForeignKey, func, String, DateTime, text, Integer, Float
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import Base


class DealKnowledgeExtractionTable(Base):
    __tablename__ = "deal_knowledge_extraction"

    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("org.id"))
    bot_id = Column(String, ForeignKey("bot.id"))
    deal_id = Column(String, ForeignKey("deal.id"))
    seconds_ago = Column(Integer, nullable=True)
    prompt_id = Column(String, ForeignKey("prompt.id"), nullable=True)
    meeting_timestamp = Column(Float, nullable=True)
    knowledge = Column(JSONB, server_default=text("'{}'"), default={})
    knowledge_text = Column(String, nullable=True)

    meta = Column(JSONB, server_default=text("'{}'"), default={})
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
