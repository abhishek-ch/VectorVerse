# main.py
import os
import tempfile
import configparser
import streamlit as st
from files import file_uploader, url_uploader
# from question import chat_with_doc
# from brain import brain
# from docgpt.config import load_config
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import SupabaseVectorStore
# from supabase import Client, create_client
# from explorer import view_document
# from stats import get_usage_today
import sqlite3
from verse.sqlite_helper import *
from sqlite3 import Connection


conn = sqlite3.connect(DB_NAME, isolation_level=None)
# cursor = conn.cursor()
print("Database created!")
create_table(conn=conn)


self_hosted = True


models = ["gpt-3.5-turbo", "gpt-4", "GPT4All", "LlamaCpp"]

# Set the theme
st.set_page_config(
    page_title="GroupDiscussion_GPT",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.title("🧠 MultiReader - Read in Style 🧠")
st.markdown("Chat with your Data using Multiple GPT Models")
if self_hosted == "false":
    st.markdown('**📢 Note: In the public demo, access to functionality is restricted. You can only use the GPT-3.5-turbo model and upload files up to 1Mb. To use more models and upload larger files, consider self-hosting Quivr.**')

st.markdown("---\n\n")

st.session_state["overused"] = False
if self_hosted == "false":
    usage = 100
    if usage > st.secrets.usage_limit:
        st.markdown(
            f"<span style='color:red'>You have used {usage} tokens today, which is more than your daily limit of {st.secrets.usage_limit} tokens. Please come back later or consider self-hosting.</span>", unsafe_allow_html=True)
        st.session_state["overused"] = True
    else:
        st.markdown(f"<span style='color:blue'>Usage today: {usage} tokens out of {st.secrets.usage_limit}</span>", unsafe_allow_html=True)
    st.write("---")
    



# Initialize session state variables
if 'model' not in st.session_state:
    st.session_state['model'] = "gpt-3.5-turbo"
if 'temperature' not in st.session_state:
    st.session_state['temperature'] = 0.0
if 'chunk_size' not in st.session_state:
    st.session_state['chunk_size'] = 500
if 'chunk_overlap' not in st.session_state:
    st.session_state['chunk_overlap'] = 0
if 'max_tokens' not in st.session_state:
    st.session_state['max_tokens'] = 256

# Create a radio button for user to choose between adding knowledge or asking a question
user_choice = st.radio(
    "Choose an action", ('Database Configuration', 'Chat with your Brain', 'Forget', "Explore"))

st.markdown("---\n\n")

if user_choice == 'Database Configuration':
    # Display chunk size and overlap selection only when adding knowledge
    # st.sidebar.title("Configuration")
    with st.sidebar:
        # st.markdown(
        #     "Choose your chunk size and overlap for adding knowledge.")
        # st.session_state['chunk_size'] = st.sidebar.slider(
        #     "Select Chunk Size", 100, 1000, st.session_state['chunk_size'], 50)
        # st.session_state['chunk_overlap'] = st.sidebar.slider(
        #     "Select Chunk Overlap", 0, 100, st.session_state['chunk_overlap'], 10)
        st.title("Database Configuration")
        # st.markdown("Upload Your Preferred Data in the Database")
        # st.subheader("Upload Your Preferred Data in the Database")
        file_uploader(conn, None)
        
        # Create two columns for the file uploader and URL uploader
        # col1, col2 = st.columns(2)
        
        # with col1:
            # file_uploader(None, None)
    # with col2:
    #     url_uploader(None, None)
elif user_choice == 'Chat with your Brain':
    # Display model and temperature selection only when asking questions
    st.sidebar.title("Configuration")
    st.sidebar.markdown(
        "Choose your models")
    if self_hosted != "false":
        st.session_state['model'] = st.sidebar.multiselect(
        "Select Model(s)", models)
    else:
        st.sidebar.write("**Model**: gpt-3.5-turbo")
        st.sidebar.write("**Self Host to unlock more models such as claude-v1 and GPT4**")
        st.session_state['model'] = "gpt-3.5-turbo"
    # st.session_state['temperature'] = st.sidebar.slider(
    #     "Select Temperature", 0.0, 1.0, st.session_state['temperature'], 0.1)
    # if st.secrets.self_hosted != "false":
    #     st.session_state['max_tokens'] = st.sidebar.slider(
    #         "Select Max Tokens", 256, 2048, st.session_state['max_tokens'], 2048)
    # else:
    #     st.session_state['max_tokens'] = 256
    
    # chat_with_doc(st.session_state['model'], vector_store, stats_db=supabase)
elif user_choice == 'Forget':
    st.sidebar.title("Configuration")

    # brain(supabase)
elif user_choice == 'Explore':
    st.sidebar.title("Configuration")
    # view_document(supabase)

st.markdown("---\n\n")