from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    database_url: str

    redis_rest_url: str
    redis_rest_token: str

    qdrant_url: str
    qdrant_api_key: str

    groq_api_key: str

    embedding_model: str = "sentence-transformersall-MiniLM-L6-v2"

    # Maximum Upload Size = 15 MB
    max_upload_size: int = 15 * 1024 * 1024

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
