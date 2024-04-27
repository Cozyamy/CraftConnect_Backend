from datetime import timedelta

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from core import CURRENT_USER_DEPENDENCY, SESSION_DEP, crud, settings
from models import Token, User
from utils import create_access_token, handle_firebase_phonenumber


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
        # check if a user with the provided Firebase email already exists
        user_exist = await crud.get_by_param(
            param=fb_mail,
            arg="email",
            db=db,
            model=User,
            op="==",
        )

        # if a user with the email already exists, raise an Exception
        if user_exist:
            raise HTTPException(
                status_code=400,
                detail=f"User with this email already exists.",
            )

        # prepare user data to be inserted into the database
        db_user: User = {
            "first_name": data.first_name,
            "last_name": data.last_name,
            "phone_number": await handle_firebase_phonenumber(data.phone_number),
            "email": fb_mail,
        }

        # create the new user in the database
        user: User = await crud.create(
            param=db_user,
            table=User,
            db=db,
        )

        # Return the newly created user object
        return db_user

    except Exception as error:
        # raise an Exception if any error occurs
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

    # extract user name and email from the provided data
    user_signing_in: dict[str, any] = {
        "name": data["name"],
        "email": data["email"],
    }

    # check if the user already exists in the database
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

        # check if the user exists and take appropriate action
        match user_exists:
            case False:
                # if the user does not exist, create a new user
                first_name, last_name = user_signing_in["name"].split(" ", 1)

                user: User = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": user_signing_in["email"],
                }

                # create the new user in the database
                db_user: User = await crud.create(
                    param=user,
                    table=User,
                    db=db,
                )

                # generate and return an access token for the new user
                return Token(
                    access=await create_access_token(
                        subject=db_user.id, expires=access_token_expires
                    )
                )

            case True:
                # if the user already exists, fetch the user from the database
                user: User = await crud.get_by_param(
                    param=user_signing_in["email"],
                    arg="email",
                    db=db,
                    model=User,
                    op="==",
                )

                # generate and return an access token for the new user
                return Token(
                    access=await create_access_token(
                        subject=user.id, expires=access_token_expires
                    )
                )

    except Exception as error:
        # raise the error if any exception occurs
        raise error


async def update_user(who: CURRENT_USER_DEPENDENCY, data: type, db: SESSION_DEP):
    """
    Update user data based on provided data and the current user's information.

    Args:
        who (CURRENT_USER_DEPENDENCY): Current user information.
        data (type): Data containing user information to update.
        db (SESSION_DEP): Database session.

    Returns:
        User: Updated user object.

    Raises:
        HTTPException: If the user is not found or an error occurs during the update.
    """

    try:
        # fetch the user from the database based on the current user's ID
        db_user: User = await crud.get_by_param(
            param=who.id,
            arg="id",
            db=db,
            model=User,
            op="==",
        )

        # check if the user exists
        if not db_user:
            raise HTTPException(
                status_code=404,
                detail=f"User not found.",
            )

        # update the user data based on the provided data
        for key, value in data.model_dump().items():
            if value is not None:
                setattr(db_user, key, value)

        # commit changes to database
        db.commit()

        # return updated information
        return db_user

    except Exception as error:
        # raise the error if any exception occurs
        raise error
