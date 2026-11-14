from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    database_url: str

    redis_rest_url: str
    redis_rest_token: str

    qdrant_url: str
    qdrant_api_key: str

    groq_api_key: str

    embedding_model: str = "sentence-transformersall-MiniLM-L6-v2"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
