import os
from langchain.docstore.document import Document
from langchain.vectorstores import VectorStore
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import FAISS

db_persistent_path = f"""{os.environ["db_persistent_path"]}/FAISS/faiss_index"""


def upload(documents: list[Document], embeddings: Embeddings) -> None:
    vectordb = FAISS.from_documents(documents=documents, embedding=embeddings)
    vectordb.save_local(db_persistent_path)
    vectordb = None


def create(embeddings: Embeddings) -> VectorStore:
    return FAISS.load_local(folder_path=db_persistent_path, embeddings=embeddings)
