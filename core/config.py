import secrets
from typing import Annotated, Any, Literal

from pydantic import AnyUrl, BaseModel


def parse_cors(value: Any) -> list[str] | str:
    if isinstance(value, str) and not value.startswith("["):
        return [item.strip() for item in value.split(",")]

    elif isinstance(value, (list, str)):
        return value

    raise ValueError(value)


class AppSettings(BaseModel):
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = secrets.token_urlsafe(32)

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    DOMAIN: str = "localhost"

    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, parse_cors] = [
        "*"
    ]  # Define default value here

    ALGORITHM: str = "HS256"

    PROJECT_NAME: str = "CraftConnect"

    PROJECT_DESCRIPTION: str = (
        "A Simple Application that connects artisans to customers with FastAPI"
    )

    SERVER_NAME: str = "CraftConnectBackend"

    SESSION_TOKEN_EXPIRE_SECONDS: int = 43200


settings = AppSettings()