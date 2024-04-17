from fastapi import APIRouter, Depends, UploadFile, File
from sqlmodel import Session
from dependencies.deps import get_db, get_current_user
from models.user_models import User, ArtisanResponse
from typing import List
from dependencies import crud

post_ad_router = APIRouter(
    tags=["Post ad"],
)

@post_ad_router.post("/artisans/create/", response_model=ArtisanResponse)
async def post_ad(
    category: str,
    price: float,
    location: str,
    description: str,
    pictures: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    crud.validate_pictures(pictures)

    user_id = current_user.id
    artisan = crud.post_ad_object(user_id, category, price, location, description)

    crud.post_ad(db, artisan, pictures)

    return {"message": "Ad posted successfully"}