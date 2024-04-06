import logging
from datetime import datetime

import click

from src.db.db import Base, get_engine, get_session
from src.repositories.user import UserRepository
from src.repositories.chat import ChatRepository
from src.schemas.user import UserSchema
from src.schemas.chat import ChatSchema

database = click.Group("database", help="Commands related to database")
logger = logging.getLogger(__name__)


@database.command()
def setup_database() -> None:
    db = get_session()
    user = UserSchema(name="ROOT", email="email@gmail.com", meta={}, created_at=datetime.now())
    chat = ChatSchema(meta={}, user_id=user.id, created_at=datetime.now())
    UserRepository(db).create(user)
    ChatRepository(db).create(chat)


@database.command()
def refresh_database() -> None:
    db = get_engine()
    Base.metadata.drop_all(bind=db)
    Base.metadata.create_all(bind=db, checkfirst=False)
