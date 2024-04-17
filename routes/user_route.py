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
from datetime import timedelta, datetime, timezone
from configurations.config import settings
import os
import uuid

api_router = APIRouter()
IMAGEDIR ='./uploaded_images/'
os.makedirs(IMAGEDIR, exist_ok=True)

@api_router.get("/", tags=["home"])
async def home():
    return {"message": "Welcome to CraftConnect!"}

@api_router.post("/register", tags=["register"])
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


@api_router.post("/login", tags=["login"])
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

@api_router.post("/artisans/create/", tags=["create artisan"], response_model=ArtisanResponse)
async def create_artisan(
    category: str,
    price: float,
    location: str,
    description: str,
    pictures: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if len(pictures) > 2:
        raise HTTPException(status_code=400, detail="Maximum 2 pictures allowed")

    if not pictures:
        raise HTTPException(status_code=400, detail="No pictures provided")

    user_id = current_user.id
    formatted_created_at = datetime.now(timezone.utc)

    artisan = Artisan(
    user_id=user_id,
    category=category,
    price=price,
    location=location,
    description=description,
    created_at=formatted_created_at
    )
    db.add(artisan)
    db.commit()
    for picture in pictures:
        file_extension = picture.filename.split(".")[-1]
        picture_path = f"{uuid.uuid4()}.{file_extension}"
        picture_path = os.path.join(IMAGEDIR, picture_path)
        with open(picture_path, "wb") as f:
            f.write(await picture.read())
        picture_db = Picture(artisan_id=artisan.id, path=picture_path)
        db.add(picture_db)
    db.commit()
    return {"message": "Artisan created successfully"}

@api_router.get("/artisans/all", response_model=Dict[str, List[ArtisanSearchResult]], tags=["browse artisans"])
async def browse_all_artisans(
    db: Session = Depends(get_db)
):
    artisans = crud.get_all_artisans(db)
    artisan_results = []
    for artisan in artisans:
        artisan_result = ArtisanSearchResult(
            id=artisan.id,
            category=artisan.category,
            price=artisan.price,
            location=artisan.location,
            description=artisan.description,
            created_at=artisan.created_at,
            user_email=artisan.user.email,
            user_first_name=artisan.user.first_name,
            user_last_name=artisan.user.last_name,
            user_phone_number=artisan.user.phone_number,
            pictures=[picture.path for picture in artisan.pictures]
        )
        artisan_results.append(artisan_result)
    return {"artisans": artisan_results}


@api_router.get("/artisans/category/{category}", response_model=List[ArtisanSearchResult], tags=["search artisans"])
async def search_artisans_by_category(
    category: str,
    db: Session = Depends(get_db)
):
    artisans = crud.get_artisans_by_category(db, category)
    artisan_results = []
    for artisan in artisans:
        artisan_result = ArtisanSearchResult(
            id=artisan.id,
            category=artisan.category,
            price=artisan.price,
            location=artisan.location,
            description=artisan.description,
            created_at=artisan.created_at,
            user_email=artisan.user.email,
            pictures=[picture.path for picture in artisan.pictures]
        )
        artisan_results.append(artisan_result)
    return artisan_results

@api_router.get("/artisans/name/{name}", response_model=List[ArtisanSearchResult], tags=["search artisans"])
async def search_artisans_by_name(
    name: str,
    db: Session = Depends(get_db)
):
    artisans = crud.get_artisans_by_name(db, name)
    artisan_results = []
    for artisan in artisans:
        artisan_result = ArtisanSearchResult(
            id=artisan.id,
            category=artisan.category,
            price=artisan.price,
            location=artisan.location,
            description=artisan.description,
            created_at=artisan.created_at,
            user_email=artisan.user.email,
            pictures=[picture.path for picture in artisan.pictures]
        )
        artisan_results.append(artisan_result)
    return artisan_results

@api_router.get("/artisans/location/{location}", response_model=List[ArtisanSearchResult], tags=["search artisans"])
async def search_artisans_by_location(
    location: str,
    db: Session = Depends(get_db)
):
    artisans = crud.get_artisans_by_location(db, location)
    artisan_results = []
    for artisan in artisans:
        artisan_result = ArtisanSearchResult(
            id=artisan.id,
            category=artisan.category,
            price=artisan.price,
            location=artisan.location,
            description=artisan.description,
            created_at=artisan.created_at,
            user_email=artisan.user.email,
            pictures=[picture.path for picture in artisan.pictures]
        )
        artisan_results.append(artisan_result)
    return artisan_results


@api_router.get("/artisans/price", response_model=List[ArtisanSearchResult], tags=["search artisans"])
async def search_artisans_by_price_range(
    min_price: float, 
    max_price: float,
    db: Session = Depends(get_db)
):
    artisans = crud.get_artisans_by_price_range(db, min_price, max_price)
    artisan_results = []
    for artisan in artisans:
        artisan_result = ArtisanSearchResult(
            id=artisan.id,
            category=artisan.category,
            price=artisan.price,
            location=artisan.location,
            description=artisan.description,
            created_at=artisan.created_at,
            user_email=artisan.user.email,
            pictures=[picture.path for picture in artisan.pictures]
        )
        artisan_results.append(artisan_result)
    return artisan_results
