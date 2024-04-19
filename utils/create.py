from datetime import datetime, timedelta, timezone

from jose import jwt

from core import settings


async def create_access_token(subject: any, expires: timedelta):
    token_expiration_time = datetime.now(timezone.utc) + expires

    created_token = jwt.encode(
        claims={"exp": token_expiration_time, "sub": str(subject)},
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return created_token
