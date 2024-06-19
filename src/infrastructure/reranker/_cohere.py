import logging

from src.infrastructure.reranker.base import RerankType, RerankerManager
from src.schemas.models import RerankModel, RerankCohereEnglishV3, cohere_rerank_table
from src import console, API_KEYS

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
            RerankType(query=query, new_index=x.index, previous_index=i, score=x.relevance_score, document=documents[i])
            for i, x in enumerate(res)
        ]

    @classmethod
    def describe_models(self):
        console.print(cohere_rerank_table)


if __name__ == "__main__":
    CohereReranker.describe_models()
    res = CohereReranker(RerankCohereEnglishV3()).rerank(
        "where is the dog?", ["you can find it here", "the dog is tired", "the dog is in the bed"], top_n=5
    )
    logger.info(res)
