import os
from langchain.docstore.document import Document
from langchain.vectorstores import VectorStore
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import Weaviate
import weaviate

db_persistent_path = f"""{os.environ["db_persistent_path"]}/chromadb"""


def upload(documents: list[Document], embeddings: Embeddings) -> None:
    Weaviate.from_documents(
        documents=documents,
        embedding=embeddings,
        weaviate_url="http://localhost:8080",
        by_text=False,
        index_name="weviate",
    )


def create(embeddings: Embeddings) -> VectorStore:
    return Weaviate(
        embedding=embeddings,
        client=weaviate.Client(url="http://localhost:8080"),
        index_name="weviate",
        text_key="text",
    )
