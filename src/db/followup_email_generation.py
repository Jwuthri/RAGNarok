# from sqlalchemy import Column, ForeignKey, func, String, DateTime, text
# from sqlalchemy.dialects.postgresql import JSONB

# from src.db.db import Base


# class FollowUpEmailTable(Base):
#     __tablename__ = "followup_email"

#     id = Column(String, primary_key=True)
#     org_id = Column(String, ForeignKey("org.id"))
#     generated_email = Column(String)
#     product_id = Column(String, ForeignKey("product.id"), nullable=True)
#     prompt_id = Column(String, ForeignKey("prompt.id"), nullable=True)
#     deal_id = Column(String, ForeignKey("deal.id"), nullable=True)
#     highlights = Column(JSONB, server_default=text("'[]'"), default=[])

#     creator_type = Column(String, nullable=True)
#     user_id = Column(String, ForeignKey("user.id"), nullable=True)

#     meta = Column(JSONB, server_default=text("'{}'"), default={})
#     created_at = Column(DateTime, server_default=func.now())
#     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
