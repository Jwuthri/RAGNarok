import logging
from sqlalchemy.orm import Session

from src.db import ProductTable
from src.schemas import ProductSchema

logger = logging.getLogger(__name__)


class ProductRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, data: ProductSchema) -> ProductSchema:
        try:
            db_record = ProductTable(**data.model_dump())
            self.db_session.add(db_record)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            logger.error(e)

        return data

    def read(self, _id: int) -> ProductSchema:
        db_record = self.db_session.query(ProductTable).filter(ProductTable.id == _id).first()

        return ProductSchema.model_validate(db_record) if db_record else None

    def read_by_name(self, name: str) -> ProductSchema:
        db_record = self.db_session.query(ProductTable).filter(ProductTable.name == name).first()

        return ProductSchema.model_validate(db_record) if db_record else None

    def update(self, _id: int, data: ProductSchema) -> ProductSchema:
        db_record = self.db_session.query(ProductTable).filter(ProductTable.id == _id).first()
        if db_record:
            for field, value in data.model_dump().items():
                if hasattr(db_record, field) and value:
                    setattr(db_record, field, value)
            self.db_session.commit()

        return ProductSchema.model_validate(db_record) if db_record else data

    def delete(self, _id: int) -> int:
        try:
            row_count = self.db_session.query(ProductTable).filter(ProductTable.id == _id).delete()
            self.db_session.commit()
            return row_count
        except Exception as e:
            logger.error(e)
            self.db_session.rollback()
            return None
