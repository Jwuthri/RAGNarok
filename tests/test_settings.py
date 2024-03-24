import os
import tempfile
from dotenv import load_dotenv
from pathlib import Path

from src.settings import *


def test_api_keys():
    with tempfile.NamedTemporaryFile(mode="w") as env_file:
        keys = {
            "PINECONE_INDEX": "test_index",
            "PINECONE_ENV": "test_pinecone_env",
            "PINECONE_API_KEY": "test_pinecone_api_key",
            "NOTION_API_KEY": "test_notion_api_key",
            "OPENAI_API_KEY": "test_openai_api_key",
            "PROMPTLAYER_API_KEY": "test_promptlayer_api_key",
            "APIFY_API_TOKEN": "test_apify_api_token",
        }
        for key, value in keys.items():
            env_file.write(f"{key}={value}\n")
        env_file.flush()

        load_dotenv(dotenv_path=Path(env_file.name), override=True)

        assert os.environ.get("PINECONE_INDEX") == keys["PINECONE_INDEX"]
        assert os.environ.get("PINECONE_ENV") == keys["PINECONE_ENV"]
        assert os.environ.get("PINECONE_API_KEY") == keys["PINECONE_API_KEY"]
        assert os.environ.get("NOTION_API_KEY") == keys["NOTION_API_KEY"]
        assert os.environ.get("OPENAI_API_KEY") == keys["OPENAI_API_KEY"]
        assert os.environ.get("PROMPTLAYER_API_KEY") == keys["PROMPTLAYER_API_KEY"]
        assert os.environ.get("APIFY_API_TOKEN") == keys["APIFY_API_TOKEN"]


def test_project_paths():
    assert PROJECT_PATHS.ROOT_PATH.is_dir()
    assert PROJECT_PATHS.PROJECT_PATH.is_dir()
    assert PROJECT_PATHS.QUERIES_PATH.is_dir()
    assert PROJECT_PATHS.DATA_PATH.is_dir()
    assert PROJECT_PATHS.EXTERNAL_DATA.is_dir()
    assert PROJECT_PATHS.INTERIM_DATA.is_dir()
    assert PROJECT_PATHS.PROCESSED_DATA.is_dir()
    assert PROJECT_PATHS.RAW_DATA.is_dir()
    assert PROJECT_PATHS.MODEL_DATA.is_dir()
