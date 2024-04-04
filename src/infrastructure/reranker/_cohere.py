import logging

from src.infrastructure.reranker.base import RerankType, RerankerManager
from src import Table, CONSOLE, API_KEYS
from src.schemas.models import RerankModel, RerankCohereEnglish

logger = logging.getLogger(__name__)


class CohereReranker(RerankerManager):
    def __init__(self, model: RerankModel) -> None:
        super().__init__()
        self.model = model
        try:
            import cohere

            self.client = cohere.Client(api_key=API_KEYS.COHERE_API_KEY)
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install cohere`")

    def rerank(self, query: str, documents: list[str], top_n: int = 5) -> list[RerankType]:
        res = self.client.rerank(model=self.model.name, query=query, documents=documents, top_n=top_n).results

        return [
            RerankType(new_index=x.index, previous_index=i, score=x.relevance_score, document=documents[i])
            for i, x in enumerate(res)
        ]

    @classmethod
    def describe_models(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("LATEST MODEL", justify="left")
        table.add_column("DESCRIPTION", justify="left")

        table.add_row("rerank-english-v2.0", "A model that allows for re-ranking English language documents.")
        table.add_row(
            "rerank-multilingual-v2.0",
            "A model for documents that are not in English. Supports the same languages as embed-multilingual-v3.0.",
        )

        CONSOLE.print(table)


if __name__ == "__main__":
    CohereReranker.describe_models()
    res = CohereReranker(RerankCohereEnglish()).rerank(
        "where is the dog?", ["you can find it here", "the dog is tired", "the dog is in the bed"]
    )
    logger.info(res)
