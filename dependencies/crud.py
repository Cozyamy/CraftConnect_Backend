from sqlmodel import Session, select
from sqlalchemy import func
from models.user_models import User, UserCreate, Artisan
from utils.utils import verify_password
from typing import List, Optional

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

def create_user(*, session: Session, email: str, user) -> User:
    user = User(email=email, first_name=user.first_name, last_name=user.last_name, phone_number=user.phone_number)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_artisans(
    db: Session, 
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    location: Optional[str] = None
) -> List[Artisan]:
    query = db.query(Artisan)

    if category:
        query = query.filter(Artisan.category == category)

    if min_price is not None:
        query = query.filter(Artisan.price >= min_price)

    if max_price is not None:
        query = query.filter(Artisan.price <= max_price)

    if location:
        query = query.filter(Artisan.location == location)

    return query.all()

def get_all_artisans(
    db: Session
) -> List[Artisan]:
    return db.query(Artisan).all()

def get_artisans_by_category(
    db: Session, 
    category: str
) -> List[Artisan]:
    return db.query(Artisan).filter(func.lower(Artisan.category) == func.lower(category)).all()

def get_artisans_by_name(
    db: Session, 
    name: str
) -> List[Artisan]:
    return db.query(Artisan).filter(Artisan.name.ilike(f"%{name}%")).all()

def get_artisans_by_location(
    db: Session, 
    location: str
) -> List[Artisan]:
    return db.query(Artisan).filter(Artisan.location.ilike(f"%{location}%")).all()

def get_artisans_by_price_range(
    db: Session, 
    min_price: float, 
    max_price: float
) -> List[Artisan]:
    return db.query(Artisan).filter(Artisan.price >= min_price, Artisan.price <= max_price).all()