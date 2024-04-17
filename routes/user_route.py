from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session
from dependencies.deps import get_db, get_current_user
from models.user_models import User, UserDetail, Token, OrderDetails, Order, UserCreate
from typing import Annotated, Any
from utils.utils import create_access_token, validate_firebase_token_header
from dependencies import crud
from datetime import timedelta
from configurations.config import settings
import logging

user_router = APIRouter(
    tags=["User"]
)

@user_router.post("/register")
async def register(
    email: Annotated[str, Depends(validate_firebase_token_header)],
    user: UserDetail,
    db: Session = Depends(get_db),
):
    try:
        user = crud.create_user(session=db, email=email, user=user)
        return JSONResponse({"message": "User created successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.post("/login")
async def login(
    db: Annotated[Session, Depends(get_db)],
    email: Annotated[str, Depends(validate_firebase_token_header)]
):
    """
    Login endpoint that collects token from firebase frontend and performs the exchange
    """
    user = crud.get_user_by_email(session=db, email=email)
    if user:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(
            access_token=create_access_token(
                user.id, expires_delta=access_token_expires
            )
        )
    else:
        raise HTTPException(status_code=400, detail="User Not Found")

@user_router.get("/user/name", response_model=User)
async def get_user_name(current_user: User = Depends(get_current_user)):
    """
    Get the name of the current user.
    """
    return current_user

def submit_order(
    order_details: OrderDetails,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    new_order = Order(
        user_id=current_user.id,
        artisan_id=order_details.artisan_id,
        location=order_details.location,
        work_details=order_details.work_details,
        serial_number=order_details.serial_number,
        category=order_details.category,
        date=order_details.date,
        status=order_details.status
    )

    current_user.orders.append(new_order)
    db.add(new_order)
    db.commit()

    return {"message": "Order submitted successfully"}