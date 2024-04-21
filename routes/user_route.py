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
import firebase_admin
from firebase_admin import auth
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


# @user_router.post("/login")
# async def login(
#     db: Annotated[Session, Depends(get_db)],
#     user: Annotated[auth.UserInfo, Depends(validate_firebase_token_header)]
# ):
#     """
#     Login endpoint that collects token from firebase frontend and performs the exchange
#     """
#     dbUser = crud.get_user_by_email(session=db, email=user.email)
#     if dbUser:
#         access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#         return Token(
#             access_token=create_access_token(
#                 dbUser.id, expires_delta=access_token_expires
#             )
#         )
#     else:
#         try:
            
#             if user.display_name:
#                 first_name, last_name = user.display_name.split(' ', 1)
#             elif user['name']:
#                 first_name, last_name = user['name'].split(' ', 1)
#             else: user
#             createdUser = crud.create_user(session=db, email=user.email, user=UserDetail(
#             first_name=first_name,
#             last_name=last_name
#         ))
#             access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#             return Token(
#                 access_token=create_access_token(
#                     createdUser.id, expires_delta=access_token_expires
#                 ))
#         except ValueError:
#             first_name = user.display_name
#             last_name = ''

@user_router.post("/login")
async def login(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[auth.UserInfo, Depends(validate_firebase_token_header)]
):
    """
    Login endpoint that collects token from firebase frontend and performs the exchange
    """
    dbUser = crud.get_user_by_email(session=db, email=user.email)
    if dbUser:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(
            access_token=create_access_token(
                dbUser.id, expires_delta=access_token_expires
            )
        )
    else:
        first_name = ''
        last_name = ''
        if user.display_name:
            try:
                first_name, last_name = user.display_name.split(' ', 1)
            except ValueError:
                first_name = user.display_name
        elif 'name' in user:
            try:
                first_name, last_name = user['name'].split(' ', 1)
            except ValueError:
                first_name = user['name']

        createdUser = crud.create_user(session=db, email=user.email, user=UserDetail(
            first_name=first_name,
            last_name=last_name
        ))
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(
            access_token=create_access_token(
                createdUser.id, expires_delta=access_token_expires
            ))

       

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