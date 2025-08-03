import logging

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from pydantic import AnyUrl
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict

from src.settings import Environment

private_key = ec.generate_private_key(ec.SECP256R1())
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
).decode()

public_pem = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
).decode()


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__", env_nested_max_split=2)

    environment: Environment = Environment.TEST
    sqlite_dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///:memory:")
    jwt_private_key: str = private_pem
    jwt_public_key: str = public_pem
    request_timeout: int = 5
    log_level: str = logging.getLevelName(logging.INFO)

    # ruff: noqa: ARG003
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (init_settings,)
