from langchain.schema import Document
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from verse.vectordb_action import search_from_vectordb


def explore_ui(vectordbs: list[str]):
    st.session_state["vectorexplore"] = st.sidebar.multiselect(
        "Select VectorDB(s)", vectordbs, key="multiselect"
    )
    layout_radio = st.sidebar.radio(
        "Layout 🌿",
        ("Concise", "Expanded"),
        key=["layout"],
        horizontal=True,
    )

    st.sidebar.markdown("---\n")

    vector_ta = st.sidebar.text_area("__Ask from Vector Database(s)?__")
    vector_ask = st.sidebar.button(
        "Ask"
    )  # ,disabled=st.session_state.vector_btn_disabled

    if vector_ask:
        if layout_radio == "Expanded":
            detailed_search(vector_ta)
        elif layout_radio == "Concise":
            concise_search(vector_ta)


def get_merged_result(documents: list[Document]) -> str:
    doc_result = ""
    for doc_tuple in documents:
        document = doc_tuple[0]
        # score = doc_tuple[1]
        page_content = document.page_content.replace("\n", "")
        metadata = document.metadata
        doc_result += page_content
        st.markdown(page_content)
        st.caption(
            f"""File: _{metadata.get("file_name")}_ | Chunk Size: _{metadata.get("chunk_size")}_ | Overlap: _{metadata.get("chunk_overlap")}_"""
        )


def publish_concise_ui(start: int, column: DeltaGenerator, query: str):
    vectordbs_selected = st.session_state["vectorexplore"]
    for idx in range(start, len(vectordbs_selected), 2):
        db = search_from_vectordb(vector_db=vectordbs_selected[idx])
        result = db.similarity_search(query)
        with column:
            st.header(vectordbs_selected[idx])
            tabs = st.tabs(list(map(str, range(1, len(result) + 1))))
            for idx in range(len(result)):
                document = result[idx]
                metadata = document.metadata
                page_content = document.page_content.replace("\n", " ")
                tabs[idx].markdown(page_content)
                tabs[idx].caption(
                    f"""File Name: _{metadata.get("file_name")}_ | Chunk Size: _{metadata.get("chunk_size")}_ | Overlap: _{metadata.get("chunk_overlap")}_"""
                )


def concise_search(query: str) -> None:
    st.session_state["vectorexplore"]
    col1, col2 = st.columns(2)
    publish_concise_ui(start=0, column=col1, query=query)
    publish_concise_ui(start=1, column=col2, query=query)


def detailed_search(query: str) -> None:
    for vector_db in st.session_state["vectorexplore"]:
        db = search_from_vectordb(vector_db=vector_db)
        result = db.similarity_search_with_score(query)
        with st.container():
            with st.expander(vector_db):
                for doc_tuple in result:
                    document = doc_tuple[0]
                    score = doc_tuple[1]
                    page_content = document.page_content.replace("\n", "")
                    metadata = document.metadata
                    st.markdown(page_content)
                    st.caption(
                        f"""File: _{metadata.get("file_name")}_ | Chunk Size: _{metadata.get("chunk_size")}_ | Overlap: _{metadata.get("chunk_overlap")}_ | Score: _{score}_"""
                    )
