from fastapi import HTTPException, Request
from firebase_admin import auth

from .format import response


async def verify_password():
    pass


async def verify_auth_token():
    pass


def verify_firebase_token(token):

    try:
        user = auth.verify_id_token(id_token=token)
        print(user)
        # print(user.get("displayName"))
        return user.get("email")
        # return user.get("displayName")

    except Exception as error:
        return response.http_error(error)
