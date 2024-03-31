import logging

from src.infrastructure.text_embedding.base import Embedding_typing, Embeddings_typing, TextEmbeddingManager
from src.utils.markdown_utils import align_markdown_table

logger = logging.getLogger(__name__)


class HuggingFaceEmbedding(TextEmbeddingManager):
    def __init__(self, model_name: str = "jinaai/jina-embeddings-v2-base-en"):
        self.model_name = model_name
        try:
            from transformers import AutoModel

            self.embeddings = AutoModel.from_pretrained(model_name, trust_remote_code=True)
            self.info_model = {
                "dimension": self.embeddings.config.hidden_size,
                "max_seq_length": self.embeddings.config.max_position_embeddings,
            }
        except ModuleNotFoundError as e:
            logger.error(e)
            logger.warning("Please run `pip install transformers`")

    def embed_batch(self, batch: list[str]) -> Embeddings_typing:
        """
        This function takes a list of strings as input and returns a list of lists of floats
        representing the embeddings of each string in the input list.
        :param batch: A list of strings representing the input data that needs to be embedded
        :type batch: list[str]
        :return: a list of lists of floats, which represent the embeddings of the input batch of
        strings.
        """
        return self.embeddings.encode(batch).tolist()

    def embed_str(self, string: str) -> Embedding_typing:
        """
        This function takes a string query and returns its embedding as a list of floats.
        :param query: A string representing the query that needs to be embedded
        :type query: str
        :return: A list of floats representing the embedding of the input query.
        """
        return self.embeddings.encode([string]).tolist()[0]

    def describe_models(self):
        logger.warning("The following table is deprecated")
        logger.info(
            align_markdown_table(
                """
            | Model Name                   | Description                                                                                                                         | Dimensions | Language     | Use Cases                          |
            |------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|------------|--------------|------------------------------------|
            | bert-base-uncased            | BERT (Bidirectional Encoder Representations from Transformers) base model                                                           | 768        | English      | General purpose sentence embedding |
            | roberta-base                 | RoBERTa (Robustly optimized BERT approach) base model                                                                               | 768        | English      | General purpose sentence embedding |
            | distilbert-base-uncased      | DistilBERT (Distilled version of BERT) base model                                                                                   | 768        | English      | General purpose sentence embedding |
            | albert-base-v2               | ALBERT (A Lite BERT) base model                                                                                                     | 768        | English      | General purpose sentence embedding |
            | electra-base                 | ELECTRA (Efficiently Learning an Encoder that Classifies Token Replacements Accurately) base model                                  | 768        | English      | General purpose sentence embedding |
            | xlnet-base-cased             | XLNet (Generalized Autoregressive Pretraining for Language Understanding) base model                                                | 768        | English      | General purpose sentence embedding |
            | camembert-base               | CamemBERT (CamemBERT: a Tasty French Language Model) base model                                                                     | 768        | French       | General purpose sentence embedding |
            | bert-base-multilingual-cased | Multilingual BERT base model                                                                                                        | 768        | Multilingual | General purpose sentence embedding |
            | xlm-roberta-base             | XLM-RoBERTa (A Robustly Optimized BERT Pretraining Approach for Cross-lingual Understanding) base model                             | 768        | Multilingual | General purpose sentence embedding |
            | facebook/bart-base           | BART (BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension) base model | 1024       | English      | Text generation, summarization     |
            | t5-small                     | T5 (Text-To-Text Transfer Transformer) small model                                                                                  | 512        | English      | Text generation, summarization     |
            | gpt2                         | GPT-2 (OpenAI's Generative Pre-trained Transformer 2) base model                                                                    | 768        | English      | Text generation, completion        |
            """
            )
        )


if __name__ == "__main__":
    x = HuggingFaceEmbedding()
    x.describe_models()
