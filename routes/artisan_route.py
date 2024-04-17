from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session
from dependencies.deps import get_db, get_current_user
from models.user_models import User, ArtisanSearchResult, ArtisanResponse
from typing import List, Dict
from dependencies import crud
from dependencies.crud import artisan_to_search_result

artisan_router = APIRouter(
    tags=["Artisan"],
)

@artisan_router.get("/artisans/all", response_model=Dict[str, List[ArtisanSearchResult]])
async def browse_all_artisans(
    db: Session = Depends(get_db)
):
    artisans = crud.get_all_artisans(db)
    artisan_results = [artisan_to_search_result(artisan) for artisan in artisans]
    return {"artisans": artisan_results}


@artisan_router.get("/artisans/category/{category}", response_model=List[ArtisanSearchResult])
async def search_artisans_by_category(category: str, db: Session = Depends(get_db)):
    artisans = crud.get_artisans_by_category(db, category)
    return [artisan_to_search_result(artisan) for artisan in artisans]

@artisan_router.get("/artisans/name/{name}", response_model=List[ArtisanSearchResult])
async def search_artisans_by_name(name: str, db: Session = Depends(get_db)):
    artisans = crud.get_artisans_by_name(db, name)
    return [artisan_to_search_result(artisan) for artisan in artisans]

@artisan_router.get("/artisans/location/{location}", response_model=List[ArtisanSearchResult])
async def search_artisans_by_location(location: str, db: Session = Depends(get_db)):
    artisans = crud.get_artisans_by_location(db, location)
    return [artisan_to_search_result(artisan) for artisan in artisans]

@artisan_router.get("/artisans/price", response_model=List[ArtisanSearchResult])
async def search_artisans_by_price_range(min_price: float, max_price: float, db: Session = Depends(get_db)):
    artisans = crud.get_artisans_by_price_range(db, min_price, max_price)
    return [artisan_to_search_result(artisan) for artisan in artisans]