from vectordbs import qdrant, chromadb, elasticsearch, faiss, pgvector, redis, weaviate
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import VectorStore

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def upload_in_vectordb(docs_with_metadata: list[Document], vector_db: str):
    match vector_db:
        case "Qdrant":
            qdrant.upload(documents=docs_with_metadata, embeddings=embeddings)
        case "Chromadb":
            chromadb.upload(documents=docs_with_metadata, embeddings=embeddings)
        case "ElasticSearch":
            elasticsearch.upload(documents=docs_with_metadata, embeddings=embeddings)
        case "FAISS":
            faiss.upload(documents=docs_with_metadata, embeddings=embeddings)
        case "PGVector":
            pgvector.upload(documents=docs_with_metadata, embeddings=embeddings)
        case "Redis":
            redis.upload(documents=docs_with_metadata, embeddings=embeddings)
        case "Weaviate":
            weaviate.upload(documents=docs_with_metadata, embeddings=embeddings)


def search_from_vectordb(vector_db: str) -> VectorStore:
    match vector_db:
        case "Qdrant":
            return qdrant.create(embeddings=embeddings)
        case "Chromadb":
            return chromadb.create(embeddings=embeddings)
        case "ElasticSearch":
            return elasticsearch.create(embeddings=embeddings)
        case "FAISS":
            return faiss.create(embeddings=embeddings)
        case "PGVector":
            return pgvector.create(embeddings=embeddings)
        case "Redis":
            return redis.create(embeddings=embeddings)
        case "Weaviate":
            return weaviate.create(embeddings=embeddings)
    return None
