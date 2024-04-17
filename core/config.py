import secrets
from typing import Annotated, Literal

from fastapi import HTTPException
from passlib.context import CryptContext
from pydantic import AnyUrl, BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(value: any) -> list[str] | str:
    """
    Parse CORS headers.

    Args:
        value (Any): Input value to parse.

    Returns:
        List[str] or str: Parsed list of strings or original input.

    Raises:
        ValueError: If the input value is neither a string nor a list.
    """

    try:
        match value:
            case value if isinstance(value, str) and not value.startswith("["):
                return [item.strip() for item in value.split(",")]

            case value if isinstance(value, (list, str)):
                return value

            case _:
                raise ValueError(f"Unsupported type: {type(value)}")

    except (Exception, HTTPException) as error:
        raise error


class AppSettings(BaseSettings):
    model_config: SettingsConfigDict = {
        "extra": "ignore",
        "env_file": ".env",
        "env_ignore_empty": True,
    }

    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = secrets.token_urlsafe(32)

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    DOMAIN: str = "localhost"

    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    # BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, parse_cors] = [
    #     "*"
    # ]  # Define default value here

    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = (
        []
    )

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
