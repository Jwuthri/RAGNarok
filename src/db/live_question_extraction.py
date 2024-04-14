from sqlalchemy import Column, ForeignKey, func, String, DateTime, text, Integer
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import Base


class LiveQuestionExtractionTable(Base):
    __tablename__ = "live_question_extraction"

    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("org.id"))
    deal_id = Column(String, ForeignKey("deal.id"))
    bot_id = Column(String, ForeignKey("bot.id"))
    seconds_ago = Column(Integer, nullable=True)
    question_extracted = Column(String, nullable=True)
    confidence = Column(Integer, nullable=True)

    meta = Column(JSONB, server_default=text("'{}'"), default={})
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
