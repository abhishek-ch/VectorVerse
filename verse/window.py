from dotenv import load_dotenv
# load_dotenv()

import os
import streamlit as st
from verse.files import file_uploader
import sqlite3
from verse.sqlite_helper import *
from verse.multichat import *
from verse.vector_explore import *

conn = sqlite3.connect(DB_NAME, isolation_level=None)
create_table(conn=conn)
self_hosted = True
# "Milvus","PGVector","Weaviate"
vectordbs = ["Qdrant", "Chromadb", "ElasticSearch", "FAISS", "Redis"]


def clear_multi():
    st.session_state.models = []
    return


# Set the theme
st.set_page_config(
    page_title="ChatAdda",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.title("🎭 VectorVerse")
st.subheader("Ⓒ Multi-Model Multi-VectorDB Exploration Hub")
# st.markdown("Chat with your Data using Multiple GPT Models")
if self_hosted == "false":
    st.markdown(
        "**📢 Note: In the public demo, access to functionality is restricted. You can only use the GPT-3.5-turbo model and upload files up to 1Mb. To use more models and upload larger files, consider self-hosting Quivr.**"
    )

st.markdown("---\n\n")

st.session_state["overused"] = False
if self_hosted == "false":
    usage = 100
    if usage > st.secrets.usage_limit:
        st.markdown(
            f"<span style='color:red'>You have used {usage} tokens today, which is more than your daily limit of {st.secrets.usage_limit} tokens. Please come back later or consider self-hosting.</span>",
            unsafe_allow_html=True,
        )
        st.session_state["overused"] = True
    else:
        st.markdown(
            f"<span style='color:blue'>Usage today: {usage} tokens out of {st.secrets.usage_limit}</span>",
            unsafe_allow_html=True,
        )
    # st.write("---")


# # Initialize session state variables
if "models" not in st.session_state:
    st.session_state["models"] = ["gpt-3.5-turbo"]
if "generated" not in st.session_state:
    st.session_state["generated"] = {}
if "past" not in st.session_state:
    st.session_state["past"] = {}
if "singlemodel" not in st.session_state:
    st.session_state["singlemodel"] = []
if "multichat_disabled" not in st.session_state:
    st.session_state["multichat_disabled"] = False
if "ta_disabled" not in st.session_state:
    st.session_state["ta_disabled"] = False
if "db_btn_disabled" not in st.session_state:
    st.session_state["db_btn_disabled"] = True
if "vector_btn_disabled" not in st.session_state:
    st.session_state["vector_btn_disabled"] = True
if "vectordbs" not in st.session_state:
    st.session_state["vectordbs"] = ["Qdrant", "Chromadb"]
if "vectorexplore" not in st.session_state:
    st.session_state["vectorexplore"] = ["Qdrant", "Chromadb"]
if "chatvectordb" not in st.session_state:
    st.session_state["chatvectordb"] = "Qdrant"


# if 'temperature' not in st.session_state:
#     st.session_state['temperature'] = 0.0
if "chunk_size" not in st.session_state:
    st.session_state["chunk_size"] = 500
if "chunk_overlap" not in st.session_state:
    st.session_state["chunk_overlap"] = 0
# if 'max_tokens' not in st.session_state:
#     st.session_state['max_tokens'] = 256


# with st.sidebar:
# Create a radio button for user to choose between adding knowledge or asking a question
user_choice = st.sidebar.radio(
    "Choose an action",
    ("VectorDB Upload", "VectorDB Explore", "Multi Chat"),
    horizontal=False,
)

if user_choice == "VectorDB Upload":
    # st.markdown("Upload Your Preferred Data in the Database")
    # st.subheader("Upload Your Preferred Data in the Database")
    file_uploader(conn, vectordbs)

elif user_choice == "VectorDB Explore":
    explore_ui(vectordbs)

elif user_choice == "Multi Chat":
    multichat_ui(conn=conn, vectordbs=vectordbs)

elif user_choice == "Forget":
    st.sidebar.title("Forget")

elif user_choice == "Explore":
    st.sidebar.title("Explore")


if __name__ == "__main__":
    load_dotenv()
    config_file_path = "config.ini"
    if "OPENAI_API_KEY" not in os.environ and not config_file_path:
        raise ValueError(
            "Environment variable OPENAI_API_KEY not found, you can set it in Project Settings"
        )

    # if not config_file_path:
    #     print("*" * 100)
    #     set_api_key()
    # else:
    #     load_config(config_file_path)

    os.environ["TOKENIZERS_PARALLELISM"] = "true"
