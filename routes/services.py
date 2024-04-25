from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Form, HTTPException, UploadFile

from controllers import create_new_service
from core import CURRENT_USER_DEPENDENCY, SESSION_DEP
from utils import response

service = APIRouter(prefix="/service", tags=["services"])


@service.post(path="/new")
async def create_service(
    category_id: Annotated[UUID, Form(...)],
    price: Annotated[float, Form(...)],
    description: Annotated[str, Form(...)],
    location: Annotated[str, Form(...)],
    images: Annotated[list[UploadFile], Form(...)],
    db_access: SESSION_DEP,
    user: CURRENT_USER_DEPENDENCY,
):

    try:
        request = await create_new_service(
            id=category_id,
            price=price,
            description=description,
            location=location,
            images=images,
            db=db_access,
            user=user,
        )

        if not request:
            raise HTTPException(
                status_code=400,
                detail=f"Error creating this service 😥.",
            )

        return response.to_json(
            status_code=200,
            status="success",
            message="Service created 😊.",
            data=None,
        )

    except HTTPException as error:
        return response.http_error(error)
