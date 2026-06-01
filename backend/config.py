from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    openai_api_key: str = "learner025"
    openai_base_url: str = "https://keygateway.arshnivlabs.com/v1"
    pinecone_api_key: str = "placeholder"
    pinecone_index_name: str = "product-strategy-index"
    pinecone_environment: str = "us-east-1"
    cors_origins: List[str] = ["http://localhost:5173"]
    max_file_size_mb: int = 50
    upload_dir: str = "./uploads"
    model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"

    class Config:
        env_file = ("../.env", ".env")   # look in project root first, then backend/
        extra = "ignore"

settings = Settings()
