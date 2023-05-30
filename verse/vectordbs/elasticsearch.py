import os
from langchain import ElasticVectorSearch
from langchain.docstore.document import Document
from langchain.vectorstores import VectorStore
from langchain.embeddings.base import Embeddings

db_persistent_path = f"""{os.environ["db_persistent_path"]}/elasticsearch"""
INDEX_NAME = "esindex"


def upload(documents: list[Document], embeddings: Embeddings) -> None:
    return ElasticVectorSearch.from_documents(
        documents,
        embeddings,
        elasticsearch_url="http://localhost:9200",
        index_name=INDEX_NAME,
    )


def create(embeddings: Embeddings) -> VectorStore:
    return ElasticVectorSearch(
        elasticsearch_url="http://localhost:9200",
        index_name=INDEX_NAME,
        embedding=embeddings,
    )
