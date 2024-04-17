from fastapi import HTTPException, UploadFile
from sqlmodel import Session, select, or_, func, and_, join
from models.user_models import User, Artisan, ArtisanSearchResult, Picture, ArtisanResponse
from utils.utils import verify_password
from typing import List
from datetime import datetime, timezone
import os
import uuid

IMAGEDIR ='./uploaded_images/'
os.makedirs(IMAGEDIR, exist_ok=True)

def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user

def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return db_user

def create_user(*, session: Session, email: str, user: User) -> User:
    user = User(email=email, first_name=user.first_name, last_name=user.last_name, phone_number=user.phone_number)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

async def post_ad(db: Session, artisan: Artisan, pictures: List[UploadFile]):
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

def validate_pictures(pictures: List[UploadFile]):
    if len(pictures) > 2:
        raise HTTPException(status_code=400, detail="Maximum 2 pictures allowed")
    if not pictures:
        raise HTTPException(status_code=400, detail="No pictures provided")

def post_ad_object(user_id: int, category: str, price: float, location: str, description: str):
    formatted_created_at = datetime.now(timezone.utc)
    return Artisan(
        user_id=user_id,
        category=category,
        price=price,
        location=location,
        description=description,
        created_at=formatted_created_at
    )

def get_all_artisans(db: Session) -> List[Artisan]:
    return db.exec(select(Artisan)).all()

def artisan_to_search_result(artisan: Artisan) -> ArtisanSearchResult:
    return ArtisanSearchResult(
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

def get_artisans_by_category(db: Session, category: str) -> List[Artisan]:
    return db.exec(
        select(Artisan).where(func.lower(Artisan.category) == func.lower(category))
    ).all()

def get_artisans_by_name(db: Session, name: str) -> List[Artisan]:
    name_parts = name.split()
    if len(name_parts) == 2:
        first_name, last_name = name_parts
        return db.exec(
            select(Artisan).select_from(join(Artisan, User)).where(
                and_(
                    func.lower(User.first_name).like(f"%{first_name.lower()}%"),
                    func.lower(User.last_name).like(f"%{last_name.lower()}%")
                )
            )
        ).all()
    else:
        return db.exec(
            select(Artisan).select_from(join(Artisan, User)).where(
                or_(
                    func.lower(User.first_name).like(f"%{name.lower()}%"),
                    func.lower(User.last_name).like(f"%{name.lower()}%")
                )
            )
        ).all()

def get_artisans_by_location(db: Session, location: str) -> List[Artisan]:
    return db.exec(
        select(Artisan).where(Artisan.location.ilike(f"%{location}%"))
    ).all()

def get_artisans_by_price_range(db: Session, min_price: float, max_price: float) -> List[Artisan]:
    return db.exec(
        select(Artisan).where(
            and_(Artisan.price >= min_price, Artisan.price <= max_price)
        )
    ).all()