import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.repositories.chat_message import ChatMessageRepository
from src.schemas.chat_message import ChatMessage
from src.db.db import get_session

chat_message_route = APIRouter(
    routes="chat_message",
    tags=["chat_message"],
    responses={404: {"description": "Not found"}},
)
logger = logging.getLogger(__name__)


@chat_message_route.post("/", response_model=ChatMessage)
async def create_chat(chat_schema: ChatMessage, db: Session = Depends(get_session)):
    try:
        return ChatMessageRepository(db).create(data=chat_schema)
    except Exception as e:
        logger.error(f"Error in create_chat", extra=e)
        return status.HTTP_400_BAD_REQUEST


@chat_message_route.get("/{chat_id}", response_model=ChatMessage)
async def read_chat(chat_id: str, db: Session = Depends(get_session)):
    try:
        return ChatMessageRepository(db).read(_id=chat_id)
    except Exception as e:
        logger.error(f"Error in read_chat", extra=e)
        return status.HTTP_400_BAD_REQUEST


@chat_message_route.delete("/{chat_id}", response_model=int)
async def delete_chat(chat_id: str, db: Session = Depends(get_session)):
    try:
        return ChatMessageRepository(db).delete(_id=chat_id)
    except Exception as e:
        logger.error(f"Error in delete_chat", extra=e)
        return status.HTTP_400_BAD_REQUEST


@chat_message_route.patch("/{chat_id}", response_model=ChatMessage)
async def update_chat(chat_id: str, chat_schema: ChatMessage, db: Session = Depends(get_session)):
    try:
        return ChatMessageRepository(db).update(_id=chat_id, data=chat_schema)
    except Exception as e:
        logger.error(f"Error in update_chat", extra=e)
        return status.HTTP_400_BAD_REQUEST
