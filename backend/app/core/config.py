import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "RAG Document Assistant API"
    VECTOR_STORE_DIR: str = os.path.join(os.path.dirname(__file__), "../../data/vector_store")
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    LLM_MODEL_NAME: str = "qwen2.5:3b"

settings = Settings()