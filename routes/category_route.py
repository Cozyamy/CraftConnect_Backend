from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from controllers.category_controller import get_or_create_category
from dependencies.deps import get_db
from models.user_models import Category 

category_router = APIRouter(
    tags=["Category"]
)


@category_router.post("/category/")
async def create_category(name: str, db: Session = Depends(get_db)):
    category = get_or_create_category(db, name)
    return category

@category_router.get("/categories/")
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return {"categories": categories}

@category_router.get("/categories/search/")
def search_categories(query: str, db: Session = Depends(get_db)):
    categories = db.query(Category).filter(Category.name.ilike(f"%{query}%")).all()

    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")

    return categories