from sqlmodel import Session, select, or_, func, and_, join
from models.user_models import User, Artisan, ArtisanSearchResult
from utils.utils import verify_password
from typing import List

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