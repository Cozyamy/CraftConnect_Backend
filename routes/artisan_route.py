from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from models.user_models import Artisan, ArtisanIn, User, Service
from controllers.artisan_controller import parse_artisan_info, validate_artisan_info, validate_picture, save_picture
from dependencies.deps import get_db, get_current_user
from sqlmodel import Session
from sqlalchemy.orm import joinedload

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
    # Check if the user's artisan details already exist
    existing_artisan = db.query(Artisan).filter(Artisan.user_id == current_user.id).first()
    if existing_artisan:
        raise HTTPException(status_code=400, detail="Artisan details already exist for this user")

    validate_artisan_info(artisan_info)
    validate_picture(picture)
    unique_filename = save_picture(picture)

    db_artisan = Artisan(**artisan_info.dict(), picture_name=unique_filename, user_id=current_user.id)
    db.add(db_artisan)
    db.commit()
    db.refresh(db_artisan)
    return {"message": "Artisan information submitted successfully"}

@artisan_router.get("/artisans")
def get_all_artisans(db: Session = Depends(get_db)):
    artisans = db.query(Artisan).options(joinedload(Artisan.user)).all()
    if not artisans:
        raise HTTPException(status_code=404, detail="No artisans found")
    return [{"id": artisan.id, "name": f"{artisan.user.first_name} {artisan.user.last_name}"} for artisan in artisans]

@artisan_router.get("/me/artisan")
async def get_my_artisan_details(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    artisan = db.query(Artisan).filter(Artisan.user_id == current_user.id).first()
    if not artisan:
        raise HTTPException(status_code=404, detail="No artisan details found")
    return artisan

@artisan_router.delete("/me/artisan")
async def delete_my_artisan_account(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    artisan = db.query(Artisan).filter(Artisan.user_id == current_user.id).first()
    if not artisan:
        raise HTTPException(status_code=404, detail="No artisan account found")

    services = db.query(Service).filter(Service.artisan_id == artisan.id).first()
    if services:
        raise HTTPException(status_code=400, detail="Please delete your services first")

    db.delete(artisan)
    db.commit()
    return {"detail": "Artisan account deleted"}