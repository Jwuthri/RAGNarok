import logging

import click

from src.db.db import get_session
from src.schemas import DiscoveryQuestionSchema
from src.repositories.product import ProductRepository
from src.utils.google_drive import download_google_sheet
from src.repositories.discovery_question import DiscoveryQuestionRepository

discovery_question = click.Group("discovery_question", help="Commands related to discovery_question")
logger = logging.getLogger(__name__)


@discovery_question.command()
@click.option("--sheet_id", "-s", type=str)
@click.option("--org", "-o", type=str)
@click.option("--product", "-p", type=str)
def download_and_store_question_discovery_to_db(sheet_id: str, org_name: str, product_name: str) -> None:
    db_session = get_session()
    data = download_google_sheet(google_sheet_id=sheet_id, worksheet_id=1, as_pandas=True)
    db_product = ProductRepository(db_session).read_by_name(name=product_name)
    if not db_product:
        raise Exception(f"Product:{product_name} is missing")
    db_org = ProductRepository(db_session).read_by_name(name=org_name)
    if not db_org:
        raise Exception(f"Org:{org_name} is missing")

    discovery_questions = [
        DiscoveryQuestionSchema(
            product_id=db_product.id, org_id=db_org.id, question=row["question"], category=row["category"]
        )
        for _, row in data.iterrows()
        if row["product_name"] == product_name
    ]
    if not discovery_questions:
        logger.info(f"No discovery_questions for Org:{org_name}/Product:{product_name}")
        return
    db_discovery_questions = DiscoveryQuestionRepository(db_session).read_by_org_prod(
        org_id=db_org.id, product_id=db_product.id
    )
    db_discovery_questions_ids = [x.id for x in db_discovery_questions]
    intersection_old_new = [x for x in discovery_questions if x.id in db_discovery_questions_ids]
    to_delete = [x for x in db_discovery_questions if x.id not in intersection_old_new]
    to_create = [x for x in discovery_questions if x.id not in intersection_old_new]
    for delete in to_delete:
        DiscoveryQuestionRepository(db_session).delete(_id=delete.id)

    for create in to_create:
        db_discovery_questions = DiscoveryQuestionRepository(db_session).create(data=create)
