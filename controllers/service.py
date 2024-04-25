from fastapi import HTTPException
from models import Category
from core import crud


async def create_new_service(
    id,
    price,
    description,
    location,
    images,
    db,
    user,
):

    min_images = 4 if user.is_premium else 1
    max_images = 8 if user.is_premium else 2

    num_of_images = len(images)

    try:
        if num_of_images < min_images or num_of_images > max_images:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid number of images. Must be between {min_images} and {max_images} images. Premium users can upload up to 8 images, while non-premium users can upload up to 2 images.",
            )

        category = await crud.get_by_param(
            param=id, arg="id", db=db, model=Category, op="=="
        )



        pass

    except Exception as error:
        raise error
