from sqlalchemy import Column, ForeignKey, func, String, DateTime, text, Integer
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import Base


class MeetingQuestionExtractionTable(Base):
    __tablename__ = "meeting_question_extraction"

    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("org.id"))
    deal_id = Column(String, ForeignKey("deal.id"))
    bot_id = Column(String, ForeignKey("bot.id"))
    question = Column(String, nullable=True)
    prompt_id = Column(String, ForeignKey("prompt.id"))

    meta = Column(JSONB, server_default=text("'{}'"), default={})
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
