import os
from langchain.docstore.document import Document
from langchain.vectorstores import VectorStore
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import Milvus


def upload(documents:list[Document],embeddings:Embeddings) -> None:
    vectordb= Milvus.from_documents(documents=documents, embedding=embeddings,connection_args={"host": "127.0.0.1", "port": "19530"})
    vectordb = None

# TODO In Construction, Create/Load Milvus isnt striaghtforward
def create(embeddings:Embeddings) -> VectorStore:
    return None