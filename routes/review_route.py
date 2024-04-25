from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from dependencies.deps import get_db, get_current_user
from models.user_models import Review, User, ReviewCreate, ReviewDisplay
from typing import List
from utils.utils import get_image_url

review_router = APIRouter(tags=["Reviews"])

@review_router.post("/reviews", response_model=Review)
def create_review(review: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_review = Review(**review.dict(), user_id=current_user.id)
    if review.choose_anonymous:
        db_review.name = "Anonymous"
    else:
        db_review.name = f"{current_user.first_name} {current_user.last_name}"
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@review_router.get("/reviews", response_model=List[ReviewDisplay])
def read_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review, User).join(User, User.id == Review.user_id).all()
    return [{"profile_picture": get_image_url(user.profile_picture), "name": review.name, "comment": review.comment, "rating": review.rating} for review, user in reviews]