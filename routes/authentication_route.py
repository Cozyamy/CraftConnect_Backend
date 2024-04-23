from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session
from dependencies.deps import get_db
from models.user_models import UserDetail
from models.config_models import Token
from typing import Annotated, Any
from utils.utils import create_access_token, validate_firebase_token_header
from dependencies import crud
from datetime import timedelta
from configurations.config import settings

authentication_router = APIRouter(
    tags=["Authentication"]
)

@authentication_router.post("/register")
async def register(
    email: Annotated[str, Depends(validate_firebase_token_header)],
    user: UserDetail,
    db: Session = Depends(get_db),
):
    try:
        user = crud.create_user(session=db, email=email, user=user)
        return JSONResponse({"message": "User created successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@authentication_router.post("/login")
async def login(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[Any, Depends(validate_firebase_token_header)]
):
    """
    Login endpoint that collects token from firebase frontend and performs the exchange
    """
    dbUser = crud.get_user_by_email(session=db, email=user['email'])
    if dbUser:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(
            access_token=create_access_token(
                dbUser.id, expires_delta=access_token_expires
            )
        )
    else:
        first_name, last_name = user['name'].split(' ', 1)
        createdUser = crud.create_user(session=db, email=user['email'], user=UserDetail(
            first_name=first_name,
            last_name=last_name
        ))
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(
            access_token=create_access_token(
                createdUser.id, expires_delta=access_token_expires
            ))