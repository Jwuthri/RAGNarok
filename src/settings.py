import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from rich.logging import RichHandler

load_dotenv(override=True)

logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True, tracebacks_suppress=[])],
)
logger = logging.getLogger(__file__)


class ModelVar(BaseSettings):
    TEMPERATURE: float = 0.2
    PRICE_PER_TOKENS_INPUT: float = 0.0015 / 1000
    PRICE_PER_TOKENS_OUTPUT: float = 0.002 / 1000
    LLM_MODEl: str = "gpt-4"


class ApiKeys(BaseSettings):
    PINECONE_ENV: str = os.environ.get("PINECONE_ENV", "")
    COMET_API_KEY: str = os.environ.get("COMET_API_KEY", "")
    NOTION_API_KEY: str = os.environ.get("NOTION_API_KEY", "")
    PINECONE_INDEX: str = os.environ.get("PINECONE_INDEX", "")
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
    APIFY_API_TOKEN: str = os.environ.get("APIFY_API_TOKEN", "")
    PINECONE_API_KEY: str = os.environ.get("PINECONE_API_KEY", "")
    PROMPTLAYER_API_KEY: str = os.environ.get("PROMPTLAYER_API_KEY", "")
    OPENAI_ORGANIZATION: str = os.environ.get("OPENAI_ORGANIZATION", "")


class ProjectPaths(BaseSettings):
    ROOT_PATH: Path = Path(__file__).parent.parent

    PROJECT_PATH: Path = ROOT_PATH / "src"
    QUERIES_PATH: Path = PROJECT_PATH / "queries"

    DATA_PATH: Path = ROOT_PATH / "data"
    LOGS_DATA: Path = DATA_PATH / "logs"
    RAW_DATA: Path = DATA_PATH / "raw"
    INTERIM_DATA: Path = DATA_PATH / "interim"
    EXTERNAL_DATA: Path = DATA_PATH / "external"
    PROCESSED_DATA: Path = DATA_PATH / "processed"

    MODEL_DATA: Path = ROOT_PATH / "models"


class ProjectEnvs(BaseSettings):
    ENV_STATE: str = os.environ.get("ENV_STATE", "production")


MODEL_VAR = ModelVar()
PROJECT_ENV = ProjectEnvs()
PROJECT_PATHS = ProjectPaths()
API_KEYS = ApiKeys()
