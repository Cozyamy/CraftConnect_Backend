from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from dependencies.deps import get_db, get_current_user
from models.user_models import User, UserUpdate, UserSchema, ArtisanSchema
from controllers.artisan_controller import save_picture, validate_picture
from configurations.config import settings
from utils.utils import get_image_url

user_router = APIRouter(
    tags=["User"]
)

@user_router.get("/user/name", response_model=User)
async def get_user_name(current_user: User = Depends(get_current_user)):
    """
    Get the name of the current user.
    """
    return current_user

@user_router.get("/user/me", response_model=UserSchema)
def get_current_user_details(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).options(joinedload(User.artisan)).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_schema = UserSchema(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        is_premium=user.is_premium,
        registered_at=user.registered_at,
        email=user.email,
        phone_number=str(user.phone_number) if user.phone_number else None,
        artisan=ArtisanSchema(**user.artisan.dict()) if user.artisan else None
    )

    if user.profile_picture:
        user_schema.profile_picture = get_image_url(user.profile_picture)
    else:
        user_schema.profile_picture = "/uploaded_images/default_profile.png"

    if user.artisan and user.artisan.picture_name:
        user_schema.artisan.picture_name = get_image_url(user.artisan.picture_name)

    return user_schema

@user_router.put("/users/me")
def update_user(
    user: UserUpdate,
    profile_picture: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    statement = select(User).where(User.id == current_user.id)
    db_user = db.exec(statement).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.model_dump().items():
        if value is not None:
            setattr(db_user, key, value)
    if profile_picture:
        validate_picture(profile_picture)
        db_user.profile_picture = save_picture(profile_picture)
    db.commit()
    return db_user

@user_router.get("/user/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.id == user_id).options(joinedload(User.artisan))).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_schema = UserSchema(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        is_premium=user.is_premium,
        registered_at=user.registered_at,
        email=user.email,
        phone_number=str(user.phone_number) if user.phone_number else None,
        artisan=ArtisanSchema(**user.artisan.dict()) if user.artisan else None
    )

    if user.profile_picture:
        user_schema.profile_picture = get_image_url(user.profile_picture)
    else:
        user_schema.profile_picture = "/uploaded_images/default_profile.png"

    if user.artisan and user.artisan.picture_name:
        user_schema.artisan.profile_name = get_image_url(user.artisan.picture_name)

    return user_schema