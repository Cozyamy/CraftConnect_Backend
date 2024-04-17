from fastapi import HTTPException
from fastapi.responses import JSONResponse

from core import SESSION_DEP, crud
from models import User
from utils import handle_firebase_phonenumber, hash_password, response


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
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "phone_number": handle_firebase_phonenumber(data.get("phone")),
            "email": fb_mail,
            "password": hash_password(data.get("password")),
        }

        db_user: User = await crud.create(
            param=new_user,
            table=User,
            db=db,
        )

        return db_user

    except HTTPException as error:
        return response.http_error(error)
