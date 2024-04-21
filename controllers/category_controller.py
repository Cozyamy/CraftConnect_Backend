from sqlmodel import Session, select, func
from models.user_models import Category

def get_or_create_category(db_session: Session, name: str) -> Category:
    category = db_session.exec(select(Category).where(func.lower(Category.name) == func.lower(name))).first()

    if not category:
        category = Category(name=name)
        db_session.add(category)
        db_session.commit()

    return category