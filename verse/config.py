import configparser
import os
import openai
from pathlib import Path


def load_config(file_path: str) -> None:
    """
    read the configuration file
    """
    config = configparser.ConfigParser()
    config.read(file_path)
    config.sections()
    if config["azure"]["openai_key"]:
        openai_key = config["azure"]["openai_key"]
        endpoint_url = config["azure"]["endpoint_url"]
        api_version = config["azure"]["api_version"]

        os.environ["OPENAI_API_TYPE"] = "azure"
        os.environ["OPENAI_API_BASE"] = endpoint_url
        os.environ["OPENAI_API_KEY"] = openai_key
        os.environ["OPENAI_API_VERSION"] = api_version

        openai.api_type = "azure"
        openai.api_key = openai_key
        openai.api_base = endpoint_url
        openai.api_version = api_version

    elif config["openai"]["openai_key"]:
        openai.api_key = config["openai"]["openai_key"]

    if config["default"]:
        os.environ[
            "db_persistent_path"
        ] = f"""{str(Path.cwd())}/{config["default"]["db_persistent_dir"]}"""
        os.environ["collection_name"] = config["default"]["collection_name"]
        os.environ["pdf_uploadpath"] = config["default"]["pdf_uploadpath"]

    if config["model"]:
        os.environ["MODEL_TYPE"] = config["model"]["MODEL_TYPE"]
        os.environ["LLAMA_EMBEDDINGS_MODEL"] = config["model"]["LLAMA_EMBEDDINGS_MODEL"]
        os.environ["MODEL_PATH"] = config["model"]["MODEL_PATH"]


def set_api_key() -> None:
    openai.api_key = os.getenv("OPENAI_API_KEY")
