from typing import Dict, Optional

from pydantic import BaseModel


class ApiResponse(BaseModel):
    status_code: int
    status: str
    message: str
    data: Optional[Dict]
