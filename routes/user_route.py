from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from dependencies.deps import get_db, get_current_user
from models.user_models import User, UserUpdate, UserSchema, ArtisanSchema
from controllers.artisan_controller import save_picture, validate_picture
from utils.utils import get_image_url
from controllers.user_controller import create_user_schema
from typing import Optional

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
    statement = select(User).where(User.id == current_user.id).options(joinedload(User.artisan))
    user = db.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return create_user_schema(user)

@user_router.get("/user/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    statement = select(User).where(User.id == user_id).options(joinedload(User.artisan))
    user = db.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return create_user_schema(user)

@user_router.put("/users/me")
def update_user(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    profile_picture: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    statement = select(User).where(User.id == current_user.id)
    db_user = db.exec(statement).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    changes_made = False
    update_dict = {"first_name": first_name, "last_name": last_name, "email": email, "phone_number": phone_number}
    for key, value in update_dict.items():
        if value is not None:
            setattr(db_user, key, value)
            changes_made = True
    if profile_picture:
        validate_picture(profile_picture)
        db_user.profile_picture = save_picture(profile_picture)
        changes_made = True
    if changes_made:
        db.commit()
        return {"message": "User details updated successfully"}
    else:
        return {"message": "No changes made"}