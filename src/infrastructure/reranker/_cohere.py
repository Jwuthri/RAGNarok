import logging

from src import API_KEYS
from src.infrastructure.reranker.base import Rerank_typing, RerankerManager
from src.utils.markdown_utils import align_markdown_table

logger = logging.getLogger(__name__)


class CohereReranker(RerankerManager):
    def __init__(self, model_name: str = "rerank-english-v2.0") -> None:
        super().__init__()
        self.model_name = model_name
        try:
            import cohere

            self.client = cohere.Client(api_key=API_KEYS.OPENAI_API_KEY)
        except ModuleNotFoundError as e:
            logger.warning("Please run `pip install cohere`")

    def rerank(self, query: str, documents: list[str], top_n: int = 5) -> Rerank_typing:
        """
        This function reranks a list of documents based on a query using a specified model and returns
        the top N results.

        :param query: The `query` parameter is a string that represents the search query for which you
        want to rerank the documents. It is used to retrieve relevant documents based on the provided
        query
        :type query: str
        :param documents: The `documents` parameter in the `rerank` function is a list of strings
        representing the documents that you want to rerank based on the given query
        :type documents: list[str]
        :param top_n: The `top_n` parameter specifies the number of top documents to be returned after
        reranking. In this case, it is set to a default value of 5, meaning that the function will
        return the top 5 reranked documents unless a different value is provided when calling the
        function, defaults to 5
        :type top_n: int (optional)
        :return: Rerank the documents for a given query
        """
        return self.client.rerank(model=self.model_name, query=query, documents=documents, top_n=top_n)

    @classmethod
    def describe_models(self):
        logger.info(
            align_markdown_table(
                """
            | LATEST MODEL             | DESCRIPTION                                                                                               |
            |--------------------------|-----------------------------------------------------------------------------------------------------------|
            | rerank-english-v2.0      | A model that allows for re-ranking English language documents.                                            |
            | rerank-multilingual-v2.0 | A model for documents that are not in English. Supports the same languages as embed-multilingual-v3.0.    |
            """
            )
        )


if __name__ == "__main__":
    CohereReranker.describe_models()
