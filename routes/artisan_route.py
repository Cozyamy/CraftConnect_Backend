from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session
from dependencies.deps import get_db, get_current_user
from models.user_models import User, Artisan, ArtisanSearchResult, Picture, ArtisanResponse
from typing import List, Dict
from dependencies import crud
from dependencies.crud import artisan_to_search_result
from datetime import datetime, timezone
import os
import uuid

artisan_router = APIRouter()
IMAGEDIR ='./uploaded_images/'
os.makedirs(IMAGEDIR, exist_ok=True)

@artisan_router.post("/artisans/create/", tags=["create artisan"], response_model=ArtisanResponse)
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

@artisan_router.get("/artisans/all", response_model=Dict[str, List[ArtisanSearchResult]], tags=["browse artisans"])
async def browse_all_artisans(
    db: Session = Depends(get_db)
):
    artisans = crud.get_all_artisans(db)
    artisan_results = [artisan_to_search_result(artisan) for artisan in artisans]
    return {"artisans": artisan_results}


@artisan_router.get("/artisans/category/{category}", response_model=List[ArtisanSearchResult], tags=["search artisans"])
async def search_artisans_by_category(category: str, db: Session = Depends(get_db)):
    artisans = crud.get_artisans_by_category(db, category)
    return [artisan_to_search_result(artisan) for artisan in artisans]

@artisan_router.get("/artisans/name/{name}", response_model=List[ArtisanSearchResult], tags=["search artisans"])
async def search_artisans_by_name(name: str, db: Session = Depends(get_db)):
    artisans = crud.get_artisans_by_name(db, name)
    return [artisan_to_search_result(artisan) for artisan in artisans]

@artisan_router.get("/artisans/location/{location}", response_model=List[ArtisanSearchResult], tags=["search artisans"])
async def search_artisans_by_location(location: str, db: Session = Depends(get_db)):
    artisans = crud.get_artisans_by_location(db, location)
    return [artisan_to_search_result(artisan) for artisan in artisans]

@artisan_router.get("/artisans/price", response_model=List[ArtisanSearchResult], tags=["search artisans"])
async def search_artisans_by_price_range(min_price: float, max_price: float, db: Session = Depends(get_db)):
    artisans = crud.get_artisans_by_price_range(db, min_price, max_price)
    return [artisan_to_search_result(artisan) for artisan in artisans]