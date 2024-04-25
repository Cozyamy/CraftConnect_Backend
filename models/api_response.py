from typing import Dict, Optional

from pydantic import BaseModel


class ApiResponse(BaseModel):
    status_code: int = 200
    status: str = "pending"
    message: str = "transacting... please wait. 🌞"
    data: Optional[Dict]


class Token(BaseModel):
    access: str
    type: str = "bearer"


class TokenID(BaseModel):
    sub: str | None = None
