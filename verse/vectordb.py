from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant
import os
from langchain.embeddings import HuggingFaceEmbeddings


class DatabaseInterface:
    db_persistent_path = f"""{os.environ["db_persistent_path"]}/qdrant"""
    COLLECTION_NAME = "qdrantcoll"

    def __init__(self):
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.qdrant_client = QdrantClient(
            path=DatabaseInterface.db_persistent_path, prefer_grpc=True
        )
        self.qdrant_db = Qdrant(
            client=self.qdrant_client,
            collection_name="qdrantcoll",
            embeddings=embeddings,
        )

    def reset(self) -> None:
        self.qdrant_db = None
        self.qdrant_client = None
