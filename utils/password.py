from core import settings


async def handle_firebase_phonenumber(value: str) -> str:
    phone_number = "".join(item for item in value if item.isdigit())
    return f"+{phone_number}"


async def hash_password(password: str) -> str:
    return settings.PASSWORD_CONTEXT.hash(password)


async def verify_password(password: str, hashed_password: str) -> bool:
    return settings.PASSWORD_CONTEXT.verify(password, hashed_password)
