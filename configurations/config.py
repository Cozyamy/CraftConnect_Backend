import secrets
from typing import Annotated, Any, Literal
from pydantic import AnyUrl, BaseModel

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, (list, str)):
        return v
    raise ValueError(v)

class Settings(BaseModel):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, parse_cors
    ] = ["*"]  # default value
    
    ALGORITHM: str = "HS256"

    PROJECT_NAME: str = "CraftConnect"
    PROJECT_DESCRIPTION: str = "A Simple Application that connects artisans to customers with FastAPI"
    SERVER_NAME: str = "CraftConnectBackend"
    SESSION_TOKEN_EXPIRE_SECONDS: int = 43200

settings = Settings()