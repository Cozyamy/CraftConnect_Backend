from fastapi import APIRouter, HTTPException

from controllers import create_new, log_in, update_user
from core import CURRENT_USER_DEPENDENCY, FIREBASE_USER_DEPENDENCY, SESSION_DEP
from models import ApiResponse, UserCreate, UserUpdate
from utils import response

auth: APIRouter = APIRouter(prefix="/auth", tags=["authentication"])


@auth.post(path="/register", response_model=ApiResponse)
async def create_user(
    user: UserCreate, token: FIREBASE_USER_DEPENDENCY, db_access: SESSION_DEP
):
    """
    Endpoint to register a new user.

    Args:
    - `user (UserCreate)`: User data for registration.
    - `token (FIREBASE_USER_DEPENDENCY)`: Firebase user token.
    - `db_access (SESSION_DEP)`: Database session.

    Returns:
    - `JSONResponse`: JSON response containing the signup status if successful.

    Raises:
    - `HTTPException`: If there's an error during user creation.
    """

    try:
        request = await create_new(
            data=user,
            db=db_access,
            fb_mail=token["email"],
        )

        if not request:
            raise HTTPException(
                status_code=400,
                detail=f"Error creating this user. Registration not completed 😥.",
            )

        return response.to_json(
            status_code=201,
            status="success",
            message="User registration completed 😀.",
            data=None,
        )

    except HTTPException as error:
        return response.http_error(error)


@auth.post(path="/login", response_model=ApiResponse)
async def log_in_user(token: FIREBASE_USER_DEPENDENCY, db_access: SESSION_DEP):
    """
    Logs in a user based on the provided email.

    Args:
    - `email (str)`: The email address of the user (obtained from the dependency injection).
    - `db_access (object)`: The database access object (obtained from the dependency injection).

    Returns:
    - `JSONResponse`: JSON response containing the login status and user data if successful.

    Raises:
    - `HTTPException`: If the user is not found (status code 404).
    """

    try:
        request = await log_in(data=token, db=db_access)

        if not request:
            raise HTTPException(
                status_code=404,
                detail=f"User not found.",
            )

        return response.to_json(
            status_code=200,
            status="success",
            message="User log in success 😊.",
            data=request.model_dump(),
        )

    except HTTPException as error:
        return response.http_error(error)


@auth.patch(path="/update-profile", response_model=ApiResponse)
async def update_user_profile(
    user: UserUpdate,
    db_access: SESSION_DEP,
    signed_in_user: CURRENT_USER_DEPENDENCY,
):

    try:
        request = await update_user(who=signed_in_user, data=user, db=db_access)

        if not request:
            raise HTTPException(
                status_code=404,
                detail=f"Profile not updated 🫤.",
            )

        return response.to_json(
            status_code=200,
            status="success",
            message="User profile updated 😊.",
            data=request.model_dump(),
        )

    except HTTPException as error:
        return response.http_error(error)
