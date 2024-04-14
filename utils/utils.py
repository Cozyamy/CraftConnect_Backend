from datetime import datetime, timedelta
from typing import Any
from configurations.config import settings
from jose import jwt, JWTError
from passlib.context import CryptContext
from models.user_models import TokenData
from pydantic import ValidationError
from fastapi import HTTPException, status, Request
from firebase_admin import auth



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token_access(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        token_data = TokenData(**payload)
    except (JWTError, ValidationError) as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return token_data

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def validate_firebase_token_header(request: Request):
    """Do Validates token for firebase if user exists or not. and returns the email of the user."""
    headers = request.headers
    jwt = headers.get('Authorization').split(" ")[-1] if headers.get('Authorization') else None
    if jwt is None:
        raise HTTPException(status_code=401, detail="Firebase Missing Token")
    try:
        user = auth.verify_id_token(jwt)
        return user.get('email')
        # there is no if statement here to check user because i'm assuming that the frontend would have alredy registerd the user and the user would have been created in the database 
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Token")