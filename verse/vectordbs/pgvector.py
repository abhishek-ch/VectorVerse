import os
from langchain.docstore.document import Document
from langchain.vectorstores import VectorStore
from langchain.embeddings.base import Embeddings
from langchain.vectorstores.pgvector import PGVector

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
    host=os.environ.get("PGVECTOR_HOST", "localhost"),
    port=int(os.environ.get("PGVECTOR_PORT", "5432")),
    database=os.environ.get("PGVECTOR_DATABASE", "thepgvector"),
    user=os.environ.get("PGVECTOR_USER", "postgres"),
    password=os.environ.get("PGVECTOR_PASSWORD", "xsIKk1_lloP"),
)


db_persistent_path = f"""{os.environ["db_persistent_path"]}/chromadb"""
COLLECTION_NAME = "pgvector"
os.environ["PGVECTOR_VECTOR_SIZE"] = "1536"


def upload(documents: list[Document], embeddings: Embeddings) -> None:
    PGVector.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection_string=CONNECTION_STRING,
        pre_delete_collection=False,
    )


def create(embeddings: Embeddings) -> VectorStore:
    return PGVector(
        connection_string=CONNECTION_STRING,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )
