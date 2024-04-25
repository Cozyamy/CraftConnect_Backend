import secrets
from typing import Literal

from passlib.context import CryptContext
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config: SettingsConfigDict = {
        "extra": "ignore",
        "env_file": ".env",
        "env_ignore_empty": True,
        "env_file_encoding": "utf-8",
    }

    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = secrets.token_urlsafe(32)

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    DOMAIN: str = "localhost"

    HOST: str = "0.0.0.0"

    PORT: int = 7000

    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    ALGORITHM: str = "HS256"

    PROJECT_NAME: str = "CraftConnect"

    PROJECT_DESCRIPTION: str = (
        "A Simple Application that connects artisans to customers with FastAPI"
    )

    SERVER_NAME: str = "CraftConnectBackend"

    SESSION_TOKEN_EXPIRE_SECONDS: int = 43200

    PASSWORD_CONTEXT: CryptContext = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
    )


settings = AppSettings()
