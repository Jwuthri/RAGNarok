import logging
from sqlalchemy.orm import Session

from src.db import DealTable
from src.schemas import DealSchema

logger = logging.getLogger(__name__)


class DealRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, data: DealSchema) -> DealSchema:
        try:
            db_record = DealTable(**data.model_dump())
            self.db_session.add(db_record)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            logger.error(e)

        return data

    def read(self, _id: int) -> DealSchema:
        db_record = self.db_session.query(DealTable).filter(DealTable.id == _id).first()

        return DealSchema.model_validate(db_record) if db_record else None

    def read_by_org(self, org_id: str) -> list[DealSchema]:
        db_records = self.db_session.query(DealTable).filter(DealTable.org_id == org_id).all()

        return [DealSchema.model_validate(db_record) for db_record in db_records] if db_records else None

    def update(self, _id: int, data: DealSchema) -> DealSchema:
        db_record = self.db_session.query(DealTable).filter(DealTable.id == _id).first()
        if db_record:
            for field, value in data.model_dump().items():
                if hasattr(db_record, field) and value:
                    setattr(db_record, field, value)
            self.db_session.commit()

        return DealSchema.model_validate(db_record) if db_record else data

    def delete(self, _id: int) -> int:
        try:
            row_count = self.db_session.query(DealTable).filter(DealTable.id == _id).delete()
            self.db_session.commit()
            return row_count
        except Exception as e:
            logger.error(e)
            self.db_session.rollback()
            return None
