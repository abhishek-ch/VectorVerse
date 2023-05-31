from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
import os
from langchain.docstore.document import Document
from langchain.vectorstores import VectorStore
from langchain.embeddings.base import Embeddings

db_persistent_path = f"""{os.environ["db_persistent_path"]}/qdrant"""
COLLECTION_NAME = "qdrantcoll"


def upload(documents: list[Document], embeddings: Embeddings) -> None:
    qdrant_doc = Qdrant.from_documents(
        documents, embeddings, path=db_persistent_path, collection_name=COLLECTION_NAME
    )
    qdrant_doc = None
    del qdrant_doc


def create(embeddings: Embeddings) -> VectorStore:
    client = QdrantClient(path=db_persistent_path, prefer_grpc=True)
    return Qdrant(client=client, collection_name=COLLECTION_NAME, embeddings=embeddings)
