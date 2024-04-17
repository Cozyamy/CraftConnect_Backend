from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from models import UserCreate
from utils import response
from core import SESSION_DEP, FIREBASE_USER_DEPENDENCY

users: APIRouter = APIRouter(prefix="/users", tags=["authentication"])


# @users.post(path="/register")
# async def create_user(user: UserCreate):

#     try:
#         return user

#     except HTTPException as error:
#         raise response.http_error(error)


@users.post(path="/register")
async def create_user(
    user: UserCreate, email: FIREBASE_USER_DEPENDENCY, db: SESSION_DEP
):
    try:
        # Simulating a condition where an exception should be raised
        if not user.mail.endswith("@example.com"):
            raise HTTPException(status_code=422, detail="Invalid email domain.")
        return user

    except HTTPException as error:
        # Here you would handle the HTTPException, perhaps logging it or modifying the error message
        return response.http_error(error)
