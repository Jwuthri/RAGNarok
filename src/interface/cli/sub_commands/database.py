import logging
from datetime import datetime

import click

from src import DATABASE_URI
from src.db.db import Base, get_engine, get_session
from src.repositories.bot import BotRepository
from src.repositories.deal import DealRepository
from src.repositories.discovery_question import DiscoveryQuestionRepository
from src.repositories.org import OrgRepository
from src.repositories.product import ProductRepository
from src.repositories.user import UserRepository
from src.repositories.chat import ChatRepository
from src.schemas.bot import BotSchema
from src.schemas.deal import DealSchema
from src.schemas.discovery_question import DiscoveryQuestionSchema
from src.schemas.org import OrgSchema
from src.schemas.product import ProductSchema
from src.schemas.user import UserSchema
from src.schemas.chat import ChatSchema

database = click.Group("database", help="Commands related to database")
logger = logging.getLogger(__name__)


@database.command()
def delete_database():
    from sqlalchemy import MetaData

    meta = MetaData()
    meta.reflect(bind=get_engine(DATABASE_URI))
    meta.drop_all(bind=get_engine(DATABASE_URI))
    # Base.metadata.create_all(bind=get_engine(DATABASE_URI), checkfirst=False)


@database.command()
def setup_database() -> None:
    db = get_session()
    user = UserSchema(name="USER", email="email@gmail.com", meta={}, created_at=datetime.now())
    org = OrgSchema(name="ORG", creator_type="user", status="active", meta={}, created_at=datetime.now())
    deal = DealSchema(
        name="DEAL", status="active", org_id=org.id, creator_type="user", meta={}, created_at=datetime.now()
    )
    product = ProductSchema(name="PRODUCT", org_id=org.id, creator_type="user", meta={}, created_at=datetime.now())
    chat = ChatSchema(meta={}, org_id=org.id, user_id=user.id, created_at=datetime.now())
    discovery = DiscoveryQuestionSchema(question="what is your product?", org_id=org.id, product_id=product.id)
    bot = BotSchema(id="BOT", org_id=org.id, deal_id=deal.id)

    UserRepository(db).create(user)
    OrgRepository(db).create(org)
    DealRepository(db).create(deal)
    ProductRepository(db).create(product)
    ChatRepository(db).create(chat)
    DiscoveryQuestionRepository(db).create(discovery)
    BotRepository(db).create(bot)


@database.command()
def refresh_database() -> None:
    db = get_engine()
    Base.metadata.drop_all(bind=db)
    Base.metadata.create_all(bind=db, checkfirst=False)
