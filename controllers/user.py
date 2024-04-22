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
        user_exist = await crud.get_by_param(
            param=fb_mail,
            arg="email",
            db=db,
            model=User,
            op="==",
        )

        if user_exist:
            raise HTTPException(
                status_code=400,
                detail=f"User with this email already exists.",
            )

        db_user: User = {
            "first_name": data.first_name,
            "last_name": data.last_name,
            "phone_number": await handle_firebase_phonenumber(data.phone_number),
            "email": fb_mail,
        }

        user: User = await crud.create(
            param=db_user,
            table=User,
            db=db,
        )

        return db_user

    except Exception as error:
        raise error


async def log_in(data: dict, db: SESSION_DEP):
    """
    Logs in a user or creates a new user if not found.

    Args:
        data (dict): User data containing name and email.
        db (SESSION_DEP): Database session.

    Returns:
        Token: Access token if login is successful.

    Raises:
        HTTPException: If there's an error during login or user creation.
    """
    
    user_signing_in: dict[str, any] = {
        "name": data["name"],
        "email": data["email"],
    }

    user_exists: bool = bool(
        await crud.get_by_param(
            param=user_signing_in["email"],
            arg="email",
            db=db,
            model=User,
            op="==",
        )
    )

    try:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        match user_exists:
            case False:
                first_name, last_name = user_signing_in["name"].split(" ", 1)

                user: User = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone_number": None,
                    "email": user_signing_in["email"],
                }

                db_user: User = await crud.create(
                    param=user,
                    table=User,
                    db=db,
                )

                return Token(
                    access=await create_access_token(
                        subject=db_user.id, expires=access_token_expires
                    )
                )

            case True:
                user: User = await crud.get_by_param(
                    param=user_signing_in["email"],
                    arg="email",
                    db=db,
                    model=User,
                    op="==",
                )

                return Token(
                    access=await create_access_token(
                        subject=user.id, expires=access_token_expires
                    )
                )

    except Exception as error:
        raise error
