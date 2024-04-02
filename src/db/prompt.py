from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.dialects.postgresql import JSONB

from src.db import Base


class PromptTable(Base):
    __tablename__ = "prompt"

    id = Column(String, primary_key=True)
    prompt = Column(JSONB)
    model_name = Column(String)
    latency = Column(Float)
    cost = Column(Float)
    prediction = Column(String)
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    created_at = Column(DateTime)
    meta = Column(JSONB, nullable=True, default={})
