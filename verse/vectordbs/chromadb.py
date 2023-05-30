import os
from langchain.docstore.document import Document
from langchain.vectorstores import VectorStore
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import Chroma

db_persistent_path = f"""{os.environ["db_persistent_path"]}/chromadb"""

def upload(documents:list[Document],embeddings:Embeddings) -> Chroma:
    vectordb= Chroma.from_documents(documents=documents, embedding=embeddings,
                                      persist_directory=db_persistent_path)
    vectordb.persist()
    vectordb = None


def create(embeddings:Embeddings) -> VectorStore:
    return Chroma(persist_directory=db_persistent_path, 
                  embedding_function=embeddings)