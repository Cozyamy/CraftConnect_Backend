from fastapi import APIRouter, Depends, File, UploadFile
from models.user_models import Artisan, ArtisanIn, User
from controllers.artisan_controller import parse_artisan_info, validate_artisan_info, validate_picture, save_picture
from dependencies.deps import get_db, get_current_user
from sqlmodel import Session

artisan_router = APIRouter(
    tags=["Artisan"]
)

@artisan_router.post("/submit_artisan_info/")
async def submit_artisan_info(
    artisan_info: ArtisanIn = Depends(parse_artisan_info),
    picture: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    validate_artisan_info(artisan_info)
    validate_picture(picture)
    unique_filename = save_picture(picture)

    db_artisan = Artisan(**artisan_info.dict(), picture_name=unique_filename, user_id=current_user.id)
    db.add(db_artisan)
    db.commit()
    db.refresh(db_artisan)
    return {"message": "Artisan information submitted successfully"}