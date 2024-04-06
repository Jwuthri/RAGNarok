import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.repositories.chat_history import ChatHistoryRepository
from src.schemas.chat_history import ChatHistorySchema
from src.db.db import get_session

chat_history_route = APIRouter(
    routes="chat_history",
    tags=["chat_history"],
    responses={404: {"description": "Not found"}},
)
logger = logging.getLogger(__name__)


@chat_history_route.get("/{chat_id}", response_model=ChatHistorySchema)
async def read_chat(chat_id: str, db: Session = Depends(get_session)):
    try:
        return ChatHistoryRepository(db).read_chat(_id=chat_id)
    except Exception as e:
        logger.error(f"Error in read_chat", extra=e)
        return status.HTTP_400_BAD_REQUEST


@chat_history_route.delete("/{chat_id}", response_model=int)
async def delete_chat(chat_id: str, db: Session = Depends(get_session)):
    try:
        return ChatHistoryRepository(db).delete_chat(_id=chat_id)
    except Exception as e:
        logger.error(f"Error in delete_chat", extra=e)
        return status.HTTP_400_BAD_REQUEST
