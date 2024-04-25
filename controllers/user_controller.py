from models.user_models import UserSchema, ArtisanSchema
from utils.utils import get_image_url

def create_user_schema(user):
    user_schema = UserSchema(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        is_premium=user.is_premium,
        registered_at=user.registered_at,
        email=user.email,
        phone_number=str(user.phone_number) if user.phone_number else None,
        artisan=ArtisanSchema(**user.artisan.dict()) if user.artisan else None
    )

    if user.profile_picture:
        user_schema.profile_picture = get_image_url(user.profile_picture)
    else:
        user_schema.profile_picture = "/uploaded_images/default_profile.png"

    if user.artisan and user.artisan.picture_name:
        user_schema.artisan.picture_name = get_image_url(user.artisan.picture_name)

    return user_schema