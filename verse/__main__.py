from verse.config import load_config, set_api_key
import os
import streamlit.web.bootstrap
import sys
from dotenv import load_dotenv

if __name__ == "__main__":
    config_file_path = "config.ini"
    if "OPENAI_API_KEY" not in os.environ and not config_file_path:
        raise ValueError(
            "Environment variable OPENAI_API_KEY not found, you can set it in Project Settings"
        )

    load_dotenv()

    os.environ["TOKENIZERS_PARALLELISM"] = "true"

    streamlit.web.bootstrap.run("verse/window.py", sys.argv[0], [], [])
