import logging
from sqlalchemy.orm import Session

from src.db import ChatMessageTable
from src.schemas import ChatMessageSchema

logger = logging.getLogger(__name__)


class ChatMessageRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, data: ChatMessageSchema) -> ChatMessageSchema:
        try:
            db_record = ChatMessageTable(**data.model_dump())
            self.db_session.add(db_record)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()

        return data

    def read(self, _id: int) -> ChatMessageTable:
        db_record = self.db_session.query(ChatMessageTable).filter(ChatMessageTable.id == _id).first()

        return ChatMessageSchema.model_validate(db_record) if db_record else None

    def read_chat(self, chat_id: int, last_n_messages: int = None) -> list[ChatMessageSchema]:
        db_records = (
            self.db_session.query(ChatMessageTable)
            .filter(ChatMessageTable.chat_id == chat_id)
            .order_by(ChatMessageTable.created_at.asc())
            .all()
        )
        if last_n_messages:
            system = db_records[:1]
            user_assistant = db_records[1:][-last_n_messages:]
            db_records = system + user_assistant
        if last_n_messages == 0:
            system = db_records[:1]
            db_records = system

        return [self.read(record.id) for record in db_records]

    def update(self, _id: int, data: ChatMessageSchema) -> ChatMessageSchema:
        db_record = self.db_session.query(ChatMessageTable).filter(ChatMessageTable.id == _id).first()
        if db_record:
            for field, value in data.model_dump().items():
                if hasattr(db_record, field) and value:
                    setattr(db_record, field, value)
            self.db_session.commit()

        return ChatMessageSchema.model_validate(db_record) if db_record else data

    def delete(self, _id: int) -> int:
        try:
            row_count = self.db_session.query(ChatMessageTable).filter(ChatMessageTable.id == _id).delete()
            self.db_session.commit()
            return row_count
        except Exception as e:
            logger.error(e)
            self.db_session.rollback()
            return None
