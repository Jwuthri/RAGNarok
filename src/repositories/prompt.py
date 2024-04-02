import logging
from sqlalchemy.orm import Session

from src.db.prompt import PromptTable
from src.schemas.prompt import PromptSchema

logger = logging.getLogger(__name__)


class PromptRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, data: PromptSchema) -> PromptSchema:
        try:
            db_record = PromptTable(**data.model_dump())
            self.db_session.add(db_record)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            logger.error(e)

        return data

    def read(self, _id: int) -> PromptTable:
        db_record = self.db_session.query(PromptTable).filter(PromptTable.id == _id).first()

        return PromptSchema.model_validate(db_record) if db_record else None

    def update(self, _id: int, data: PromptSchema) -> PromptSchema:
        db_record = self.db_session.query(PromptTable).filter(PromptTable.id == _id).first()
        if db_record:
            for field, value in data.model_dump().items():
                if hasattr(db_record, field) and value:
                    setattr(db_record, field, value)
            self.db_session.commit()

        return PromptSchema.model_validate(db_record) if db_record else data

    def delete(self, _id: int) -> int:
        try:
            row_count = self.db_session.query(PromptTable).filter(PromptTable.id == _id).delete()
            self.db_session.commit()
            return row_count
        except Exception as e:
            logger.error(e)
            self.db_session.rollback()
            return None
