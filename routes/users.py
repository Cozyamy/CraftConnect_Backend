from fastapi import APIRouter, HTTPException

from controllers import create_new
from core import FIREBASE_USER_DEPENDENCY, SESSION_DEP
from models import UserBase, UserCreate
from utils import response

users: APIRouter = APIRouter(prefix="/users", tags=["authentication"])


@users.post(path="/register", response_model=UserBase)
async def create_user(
    user: UserCreate, email: FIREBASE_USER_DEPENDENCY, db_access: SESSION_DEP
):

    try:
        request = await create_new(
            data=user,
            db=db_access,
            fb_email=email,
        )

        if not request:
            raise HTTPException(
                status_code=400,
                detail=f"Error creating this user. Registration not completed.",
            )

        return response.to_json(
            status_code=201,
            status="success",
            message="User registratin completed.",
        )

    except HTTPException as error:
        return response.http_error(error)


# @users.post(path="/register")
# async def create_user(
#     user: UserCreate, email: FIREBASE_USER_DEPENDENCY, db: SESSION_DEP
# ):
#     try:
#         # Simulating a condition where an exception should be raised
#         if not user.mail.endswith("@example.com"):
#             raise HTTPException(status_code=422, detail="Invalid email domain.")
#         return user

#     except HTTPException as error:
#         # Here you would handle the HTTPException, perhaps logging it or modifying the error message
#         return response.http_error(error)
