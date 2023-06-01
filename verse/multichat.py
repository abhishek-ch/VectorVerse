from typing import List
import streamlit as st
from verse.models.llm import *
from streamlit.delta_generator import DeltaGenerator
from langchain.chains import RetrievalQA
from verse.vectordb import *
from verse.config import *
from streamlit_chat import message
from langchain.schema import BaseRetriever
from sqlite_helper import *
from verse.vectordb_action import search_from_vectordb
from verse.prompt import PROMPT
from verse.models import helper

models = helper.models


def multichat_ui(conn: Connection, vectordbs: list[str]) -> None:
    st.session_state["chatvectordb"] = st.sidebar.selectbox(
        "Select Vector Database", vectordbs, key="selectvectordb"
    )
    st.sidebar.markdown("---\n")
    with st.sidebar.expander("Model Configuration"):
        exec_choice = st.radio(
            "Chat with ? Model", ("All", "Specific"), horizontal=True
        )

        if exec_choice == "Specific":
            st.session_state["singlemodel"] = st.selectbox(
                "Select Model", models, key="singleselect"
            )
        else:
            st.session_state["models"] = st.multiselect(
                "Select Model(s)", models, key="multiselect"
            )
            st.session_state["singlemodel"] = []

    if len(st.session_state["models"]) > 0:
        st.session_state["ta_disabled"] = False
    else:
        st.session_state["ta_disabled"] = True

    txt_result = st.sidebar.text_area(
        "Do you have questions from the document(s)?",
        disabled=st.session_state.ta_disabled,
    )
    btnResult = st.sidebar.button("Ask", disabled=st.session_state.ta_disabled)
    tablist = chat_ui(conn, st.session_state["models"], st.session_state["singlemodel"])
    if exec_choice == "All" and btnResult:
        process_query(conn, txt_result, st.session_state["models"], tablist)
    elif exec_choice == "Specific" and btnResult:
        process_query(conn, txt_result, [st.session_state["singlemodel"]], tablist)


def chat_ui(
    conn: Connection, models: List[str], single_model: str
) -> list[DeltaGenerator]:
    if single_model:
        ref_models = [single_model]
    else:
        ref_models = models

    if ref_models:
        tab_list = st.tabs(ref_models)
        for idx, tab in enumerate(tab_list):
            with tab:
                with st.empty():
                    update_chat(
                        model=ref_models[idx],
                        records=fetch_history(conn=conn, model=ref_models[idx]),
                    )
        return tab_list
    return None


def update_chat(model: str, records: List[Any]):
    st.session_state.generated[model] = records
    if st.session_state.generated[model]:
        records = st.session_state.generated[model]
        try:
            with st.container():
                for row in records:
                    message(
                        row[3],
                        is_user=True,
                        key=str(row[0]) + f"_{model}_ques",
                        avatar_style="adventurer",
                    )
                    message("", key=str(row[0]) + f"_{model}", avatar_style="bottts")
                    st.markdown(row[4])
                    st.caption(f""":link: {row[5]} :clock1: {row[6]} """)
        except st.errors.DuplicateWidgetID:
            # A Hack when you search while keeping the tab active, recent response goes to the end,
            # once refresh ut reset back to the top.
            pass


def update_chat_window(
    conn: Connection,
    query: str,
    curr_model: str,
    llm: BaseLLM,
    retriever: BaseRetriever,
) -> None:
    st.session_state.generated[curr_model] = []
    chain_type_kwargs = {"prompt": PROMPT, "verbose": False}
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs,
    )
    # ConversationalRetrievalChain.from_llm(llm=llm, retriever =retriever, chain_type="stuff", return_source_documents=True)
    result = qa({"query": query})
    answer, sources = result["result"], result["source_documents"]
    src = {}
    for document in sources:
        doc_source = document.metadata["file_name"]
        page = document.metadata["page"]
        if doc_source in src:
            src[doc_source].append(str(page))
        else:
            src[doc_source] = [str(page)]
    src_result = ""
    for key, values in src.items():
        unique_values = ' '.join(set(values))
        src_result += f" _{key}_ __Page: {unique_values}__"
        src_result += "| "
    insert_chathistory(
        conn=conn,
        model=curr_model,
        question=query,
        answer=answer,
        source=src_result,
    )
    update_chat(model=curr_model, records=fetch_history(conn=conn, model=curr_model))


def execute_model(
    conn: Connection, query: str, model: str, tab: DeltaGenerator
) -> None:
    vectorDB = search_from_vectordb(st.session_state["chatvectordb"])
    retriever = vectorDB.as_retriever()
    with tab:
        with st.container():
            update_chat_window(
                conn=conn,
                query=query,
                curr_model=model,
                llm=get_model(model),
                retriever=retriever,
            )


def process_query(
    conn: Connection, query: str, models: List[str], tablist: List[DeltaGenerator]
):
    for idx, _ in enumerate(tablist):
        curr_tab = tablist[idx]
        curr_model = models[idx]
        execute_model(conn=conn, query=query, model=curr_model, tab=curr_tab)
