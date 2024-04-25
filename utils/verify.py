from firebase_admin import auth
from jose import JWTError, jwt

from core import settings
from models import TokenID


def verify_auth_token(token: str):

    try:
        payload = jwt.decode(
            token=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        user = TokenID(**payload)

    except (JWTError, Exception) as error:
        raise error

    return user


def verify_firebase_token(token):

    try:
        user: dict = auth.verify_id_token(id_token=token)
        return user

    except Exception as error:
        raise error
