from datetime import timedelta

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from core import SESSION_DEP, crud, settings
from models import Token, User
from utils import create_access_token, handle_firebase_phonenumber, response


async def create_new(data: dict, db: SESSION_DEP, fb_mail) -> User | JSONResponse:
    """
    Create a new user based on the provided data and Firebase email.

    Args:
        data (dict): User data including first_name, last_name, phone, and password.
        db (SESSION_DEP): Database session.
        fb_mail (str): Firebase email.

    Returns:
        User: Newly created user object.

    Raises:
        HTTPException: If there's an error during user creation.
    """

    try:
        new_user: User = {
            "first_name": data.first_name,
            "last_name": data.last_name,
            "phone_number": await handle_firebase_phonenumber(data.phone_number),
            "email": fb_mail,
        }

        db_user: User = await crud.create(
            param=new_user,
            table=User,
            db=db,
        )

        return new_user

    except HTTPException as error:
        return response.http_error(error)


async def log_in(data: any, db: SESSION_DEP):

    try:
        user: User = crud.get_by_param(
            param=data,
            arg="email",
            db=db,
            model=User,
            op="==",
        )

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        return Token(
            access=await create_access_token(
                subject=user.id, expires=access_token_expires
            )
        )

    except HTTPException as error:
        return response.http_error(error)
