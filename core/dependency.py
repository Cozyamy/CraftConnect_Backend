from typing import Annotated, Generator

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from fastapi.responses import JSONResponse

from models import User
from utils import response, verify_auth_token, verify_firebase_token

from .config import settings
from .database import engine

OAUTH2_URL = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/")


def db_session() -> Generator[Session, None, None]:
    """
    Context manager to yield a database session.

    Returns:
        Generator[Session, None, None]: SQLModel session generator.
    """

    with Session(engine) as session:
        yield session


SESSION_DEP = Annotated[Session, Depends(db_session)]
TOKEN_DEP = Annotated[str, Depends(OAUTH2_URL)]


def get_current_user(session: SESSION_DEP, token: TOKEN_DEP) -> User | JSONResponse:
    """
    Get the current user based on the provided session and token.

    Args:
        session (SESSION_DEP): Database session or connection.
        token (TOKEN_DEP): Authentication token.

    Returns:
        User: The current user if found.

    Raises:
        HTTPException: If user is not found or there's an authentication error.
    """

    try:
        token_data = verify_auth_token(token)
        user = session.get(User, token_data.sub)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found.",
            )

        return user

    except HTTPException as error:
        return response.http_error(error)


CURRENT_USER_DEPENDENCY = Annotated[User, Depends(get_current_user)]


def get_firebase_current_user(request: Request) -> str | JSONResponse:
    """
    Get the current Firebase user based on the request headers.

    Args:
        request (Request): FastAPI request object.

    Returns:
        str: User email if token is valid.

    Raises:
        HTTPException: If Firebase token is missing or invalid.
    """

    try:
        headers = request.headers
        auth_header = headers.get("Authorization", None)

        if not auth_header:
            raise HTTPException(
                status_code=401,
                detail="Firebase token not provided.",
            )

        token = auth_header.split(" ")[-1]

        return verify_firebase_token(token)

    except Exception as error:
        raise error


FIREBASE_USER_DEPENDENCY = Annotated[str, Depends(get_firebase_current_user)]
