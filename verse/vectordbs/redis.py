import os
from langchain.docstore.document import Document
from langchain.vectorstores import VectorStore
from langchain.embeddings.base import Embeddings
from langchain.vectorstores.redis import Redis


db_persistent_path = f"""{os.environ["db_persistent_path"]}/chromadb"""
INDEX_NAME = "redisindex"
os.environ["PGVECTOR_VECTOR_SIZE"] = "1536"

def upload(documents:list[Document],embeddings:Embeddings) -> None:
    Redis.from_documents(documents, embeddings,
                                    redis_url="redis://localhost:6379",  
                                    index_name=INDEX_NAME)


def create(embeddings:Embeddings) -> VectorStore:
    return Redis.from_existing_index(embeddings, 
                                     redis_url="redis://localhost:6379", 
                                     index_name=INDEX_NAME)