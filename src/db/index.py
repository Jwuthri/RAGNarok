from sqlalchemy import Column, ForeignKey, func, String, DateTime, text
from sqlalchemy.dialects.postgresql import JSONB

from src.db.db import Base


class IndexTable(Base):
    __tablename__ = "index_data"

    id = Column(String, primary_key=True)
    content = Column(String)
    org_id = Column(String, ForeignKey("org.id"))
    product_id = Column(String, ForeignKey("product.id"))

    meta = Column(JSONB, server_default=text("'{}'"), default={})
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
