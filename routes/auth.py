from fastapi import APIRouter, HTTPException

from controllers import create_new, log_in
from core import FIREBASE_USER_DEPENDENCY, SESSION_DEP
from models import UserBase, UserCreate
from utils import response

auth: APIRouter = APIRouter(prefix="/auth", tags=["authentication"])


@auth.post(path="/register", response_model=UserBase)
async def create_user(
    user: UserCreate, email: FIREBASE_USER_DEPENDENCY, db_access: SESSION_DEP
):
    """
    Endpoint to register a new user.

    Args:
    - `user (UserCreate)`: User data for registration.
    - `email (FIREBASE_USER_DEPENDENCY)`: Firebase user email.
    - `db_access (SESSION_DEP)`: Database session.

    Returns:
    - `JSONResponse`: JSON formatted response.

    Raises:
    - `HTTPException`: If there's an error during user creation.
    """

    try:
        request = await create_new(
            data=user,
            db=db_access,
            fb_mail=email,
        )

        if not request:
            raise HTTPException(
                status_code=400,
                detail=f"Error creating this user. Registration not completed.",
            )

        return response.to_json(
            status_code=201,
            status="success",
            message="User registration completed.",
            data=None,
        )

    except HTTPException as error:
        return response.http_error(error)


@auth.post("/login")
async def log_in_user(email: FIREBASE_USER_DEPENDENCY, db_access: SESSION_DEP):

    try:
        request = await log_in(data=email, invoke_db=db_access)

        if not request:
            raise HTTPException(
                status_code=404,
                detail=f"User not found.",
            )

        return response.to_json(
            status_code=200,
            status="success",
            message="User logged in success.",
            data=None,
        )

    except HTTPException as error:
        return response.http_error(error)
