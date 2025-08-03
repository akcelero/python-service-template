import logging
from enum import StrEnum
from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    TEST = "test"
    LOCAL = "local"
    DEV = "dev"
    STG = "stg"
    PROD = "prod"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__", env_nested_max_split=2)

    environment: Environment
    postgres_dsn: PostgresDsn
    jwt_public_key: str
    request_timeout: int = 5
    log_level: str = logging.getLevelName(logging.INFO)


@lru_cache
def get_settings() -> Settings:
    return Settings()
