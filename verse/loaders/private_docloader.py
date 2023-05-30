from langchain.vectorstores import Qdrant

# from docgpt.config import *
# from langchain.embeddings.openai import OpenAIEmbeddings
# from docgpt.llm import ChatLLM
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant

# from docgpt.config import *
import os
from langchain.embeddings import HuggingFaceEmbeddings
from sqlite_helper import *


class PrivateDocLoader:
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def __init__(self):
        self.db_persistent_path = os.environ["db_persistent_path"]
        self.collection_name = os.environ["collection_name"]
        self.pdf_uploadpath = os.environ["pdf_uploadpath"]

    def drop_collection(self):
        qdrant_client = QdrantClient(path=self.db_persistent_path, prefer_grpc=True)
        print(
            f"Dropping Collection {self.collection_name} SELF {qdrant_client.get_collections().collections}"
        )
        coll_names = list(
            map(lambda x: x.name, qdrant_client.get_collections().collections)
        )
        for name in coll_names:
            qdrant_client.delete_collection(collection_name=name)
        del qdrant_client

    def upload(self, documents) -> None:
        qdrant_doc = Qdrant.from_documents(
            documents,
            PrivateDocLoader.embeddings,
            path=self.db_persistent_path,
            collection_name=self.collection_name,
        )
        # ChatLLM(model=model,database=None)
        qdrant_doc = None
        del qdrant_doc
