from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./local.db"
    redis_url: str = "redis://localhost:6379/0"
    api_key: str = "changeme"
    max_file_size_mb: int = 20
    save_samples: bool = False
    model_registry: str = "models"
    active_model_version: str = "v1-baseline"

    class Config:
        env_file = ".env.example"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
