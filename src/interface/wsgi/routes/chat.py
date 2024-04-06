import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.repositories.chat import ChatRepository
from src.schemas.chat import ChatSchema
from src.db.db import get_session

chat_route = APIRouter(
    routes="chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)
logger = logging.getLogger(__name__)


@chat_route.post("/", response_model=ChatSchema)
async def create_chat(chat_schema: ChatSchema, db: Session = Depends(get_session)):
    try:
        return ChatRepository(db).create(data=chat_schema)
    except Exception as e:
        logger.error(f"Error in create_chat", extra=e)
        return status.HTTP_400_BAD_REQUEST


@chat_route.get("/{chat_id}", response_model=ChatSchema)
async def read_chat(chat_id: str, db: Session = Depends(get_session)):
    try:
        return ChatRepository(db).read(_id=chat_id)
    except Exception as e:
        logger.error(f"Error in read_chat", extra=e)
        return status.HTTP_400_BAD_REQUEST


@chat_route.delete("/{chat_id}", response_model=int)
async def delete_chat(chat_id: str, db: Session = Depends(get_session)):
    try:
        return ChatRepository(db).delete(_id=chat_id)
    except Exception as e:
        logger.error(f"Error in delete_chat", extra=e)
        return status.HTTP_400_BAD_REQUEST


@chat_route.patch("/{chat_id}", response_model=ChatSchema)
async def update_chat(chat_id: str, chat_schema: ChatSchema, db: Session = Depends(get_session)):
    try:
        return ChatRepository(db).update(_id=chat_id, data=chat_schema)
    except Exception as e:
        logger.error(f"Error in update_chat", extra=e)
        return status.HTTP_400_BAD_REQUEST
