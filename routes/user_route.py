from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from dependencies.deps import get_db, get_current_user
from models.user_models import UserCreate, User, UserDetail, Token, UserOutput, Artisan, ArtisanSearchResult, CategoriesResponse, Picture, ArtisanResponse
from typing import Annotated, Any, List, Dict
from fastapi.security import OAuth2PasswordRequestForm
from utils.utils import create_access_token, validate_firebase_token_header,  get_user_id
from dependencies import crud
from dependencies.crud import artisan_to_search_result
from datetime import timedelta, datetime, timezone
from configurations.config import settings
import os
import uuid

user_router = APIRouter()
IMAGEDIR ='./uploaded_images/'
os.makedirs(IMAGEDIR, exist_ok=True)

@user_router.get("/", tags=["home"])
async def home():
    return {"message": "Welcome to CraftConnect!"}

@user_router.post("/register", tags=["register"])
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


@user_router.post("/login", tags=["login"])
async def login(
    db: Annotated[Session, Depends(get_db)],
    email: Annotated[str, Depends(validate_firebase_token_header)]
):
    """
    Login endpoint that collects token from firebase frontend and performs the exchange
    """
    user = crud.get_user_by_email(session=db, email=email)
    if user:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(
            access_token=create_access_token(
                user.id, expires_delta=access_token_expires
            )
        )
    else:
        raise HTTPException(status_code=400, detail="User Not Found")