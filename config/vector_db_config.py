from pydantic_settings import BaseSettings


class VectorDBConfig(BaseSettings):
    type: str = "chroma"
    chroma_persist_dir: str = "./chroma_db"
    faiss_index_path: str = "./faiss_index"
    pinecone_index_name: str = "langchain-docs"
    pinecone_environment: str = "us-west1-gcp"

    class Config:
        env_prefix = "VECTOR_DB_"
        extra = "ignore"
