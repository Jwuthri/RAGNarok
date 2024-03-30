from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()


class PromptTable(Base):
    __tablename__ = "prompt"

    id = Column(Integer, primary_key=True)
    prompt = Column(JSONB)
    model_name = Column(String)
    latency = Column(Float)
    cost = Column(Float)
    prediction = Column(String)
    created_at = Column(DateTime)
