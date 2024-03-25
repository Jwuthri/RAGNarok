import os
import logging
from pathlib import Path

from dotenv import load_dotenv
from rich.logging import RichHandler
from pydantic_settings import BaseSettings
from pythonjsonlogger.jsonlogger import JsonFormatter

load_dotenv(override=True)


class LLMvalues(BaseSettings):
    TEMPERATURE: float = 0.0
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
    LOG_LVL: str = os.environ.get("LOG_LVL", "INFO")


LLM_VALUES = LLMvalues()
PROJECT_ENV = ProjectEnvs()
PROJECT_PATHS = ProjectPaths()
API_KEYS = ApiKeys()


def get_handler():
    return ["datadog"] if PROJECT_ENV.ENV_STATE == "PROD" else ["console"]


def get_level():
    return "INFO" if PROJECT_ENV.ENV_STATE == "PROD" else PROJECT_ENV.LOG_LVL


class RichCustomFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rich_handler = RichHandler(rich_tracebacks=True, tracebacks_suppress=[], tracebacks_show_locals=True)

    def format(self, record):
        return super().format(record)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "console": {
            "()": RichCustomFormatter,
            "format": "%(message)s",
            "datefmt": "<%d %b %Y | %H:%M:%S>",
        },
        "json_datadog": {
            "()": JsonFormatter,
            "format": "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
            "[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s "
            "dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] - %(message)s",
            "datefmt": "<%d %b %Y | %H:%M:%S>",
        },
    },
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "level": PROJECT_ENV.LOG_LVL,
            "formatter": "console",
            "rich_tracebacks": True,
            "tracebacks_show_locals": True,
        },
        "datadog": {
            "class": "logging.StreamHandler",
            "formatter": "json_datadog",
        },
    },
    "loggers": {
        "": {
            "handlers": get_handler(),
            "level": "INFO",
            "propagate": True,
        },
        "sentence_transformers": {
            "handlers": get_handler(),
            "level": get_level(),
            "propagate": False,
        },
        "uvicorn": {
            "handlers": get_handler(),
            "level": get_level(),
            "propagate": False,
        },
        "openai": {
            "handlers": get_handler(),
            "level": get_level(),
            "propagate": False,
        },
        "ably": {
            "handlers": get_handler(),
            "level": get_level(),
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "handlers": get_handler(),
            "level": get_level(),
            "propagate": False,
        },
    },
}

logging.captureWarnings(True)
logging.config.dictConfig(LOGGING_CONFIG)
