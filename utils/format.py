from typing import Optional

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from models import ApiResponse


class Response:

    def __init__(self) -> None:
        pass

    # api response handler
    def to_json(
        self,
        status_code: int,
        status: str,
        message: str,
        data: Optional[dict],
    ) -> JSONResponse:
        """
        Converts data into JSONResponse format.

        Args:
            status_code (int): HTTP status code.
            status (str): Status of the response.
            message (str): Message to be included in the response.
            data (Optional[dict]): Data to be included in the response.

        Returns:
            JSONResponse: JSON formatted response.
        """

        api_response = ApiResponse(
            data=data, message=message, status=status, status_code=status_code
        )

        return JSONResponse(
            status_code=status_code,
            content=api_response.model_dump(),
        )

    # http error handler
    def http_error(self, error: HTTPException) -> JSONResponse:
        """
        Handles HTTP exceptions and converts them into JSONResponse format.

        Args:
            error (HTTPException): HTTP exception object.

        Returns:
            JSONResponse: JSON formatted response for the error.
        """

        status_code: int = int(error.status_code)
        status: str = "error"
        message: str = str(error.detail)

        return self.to_json(
            status=status, message=message, status_code=status_code, data=None
        )


response = Response()
