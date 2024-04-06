import logging
from sqlalchemy.orm import Session

from src.db.chat_history import ChatHistoryTable
from src.schemas.chat_history import ChatHistorySchema

logger = logging.getLogger(__name__)


class ChatHistoryRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, data: ChatHistorySchema) -> ChatHistorySchema:
        try:
            db_record = ChatHistoryTable(**data.model_dump())
            self.db_session.add(db_record)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            logger.error(e)

        return data

    def read(self, _id: int) -> ChatHistoryTable:
        db_record = self.db_session.query(ChatHistoryTable).filter(ChatHistoryTable.id == _id).first()

        return ChatHistorySchema.model_validate(db_record) if db_record else None

    def read_chat(self, _id: int) -> list[ChatHistoryTable]:
        db_records = self.db_session.query(ChatHistoryTable).filter(ChatHistoryTable.chat_id == _id).all()

        return [ChatHistorySchema.model_validate(db_record) for db_record in db_records]

    def update(self, _id: int, data: ChatHistorySchema) -> ChatHistorySchema:
        db_record = self.db_session.query(ChatHistoryTable).filter(ChatHistoryTable.id == _id).first()
        if db_record:
            for field, value in data.model_dump().items():
                if hasattr(db_record, field) and value:
                    setattr(db_record, field, value)
            self.db_session.commit()

        return ChatHistorySchema.model_validate(db_record) if db_record else data

    def delete(self, _id: int) -> int:
        try:
            row_count = self.db_session.query(ChatHistoryTable).filter(ChatHistoryTable.id == _id).delete()
            self.db_session.commit()
            return row_count
        except Exception as e:
            logger.error(e)
            self.db_session.rollback()
            return None

    def delete_chat(self, _id: int) -> int:
        try:
            row_count = self.db_session.query(ChatHistoryTable).filter(ChatHistoryTable.chat_id == _id).delete()
            self.db_session.commit()
            return row_count
        except Exception as e:
            logger.error(e)
            self.db_session.rollback()
            return None
