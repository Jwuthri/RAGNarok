from sqlalchemy import Column, ForeignKey, func, String, DateTime, text, Integer, Boolean, Float
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import Base


class AskAboutTable(Base):
    __tablename__ = "ask_about"

    id = Column(String, primary_key=True)
    chat_id = Column(String, ForeignKey("chat.id"), nullable=True)
    prompt_id = Column(String, ForeignKey("prompt.id"), nullable=True)

    org_id = Column(String, ForeignKey("org.id"))
    org_name = Column(String, nullable=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=True)
    creator_type = Column(String, nullable=True)
    product_id = Column(String, ForeignKey("product.id"), nullable=True)
    product_name = Column(String, nullable=True)
    deal_id = Column(String, ForeignKey("deal.id"), nullable=True)
    deal_name = Column(String, nullable=True)

    answer = Column(String)
    summary = Column(String)
    follow_up = Column(String)
    confidence = Column(Integer)
    inscope = Column(Boolean)
    intent = Column(String)

    qa_type = Column(String)
    latency = Column(Float)
    cost = Column(Float)

    source_urns = Column(JSONB, default=[])
    answer_blob = Column(JSONB, default={})
    video_urn = Column(JSONB, default={})
    image_urn = Column(JSONB, default={})
    roadmap = Column(JSONB, default=[])
    fuds = Column(JSONB, default=[])
    knowledge_data = Column(JSONB, default=[])

    answered_from_cache = Column(Boolean)
    use_cache = Column(Boolean)

    meta = Column(JSONB, server_default=text("'{}'"), default={})
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
