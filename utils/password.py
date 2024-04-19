async def handle_firebase_phonenumber(value: str) -> str:
    phone_number = "".join(item for item in value if item.isdigit())
    return f"+{phone_number}"
