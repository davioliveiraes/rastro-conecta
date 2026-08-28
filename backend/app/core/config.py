from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Rastro API"
    app_env: str = "development"
    debug: bool = False
    api_version: str = "v1"


@lru_cache
def get_settings() -> Settings:
    return Settings()

