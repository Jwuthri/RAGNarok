from sqlalchemy import Column, Integer, String, DateTime, Float, func
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import Base


class PromptTable(Base):
    __tablename__ = "prompt"

    id = Column(String, primary_key=True)
    prompt = Column(JSONB)
    llm_name = Column(String)
    latency = Column(Float)
    cost = Column(Float)
    prediction = Column(String)
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    meta = Column(JSONB, nullable=True, default={})
