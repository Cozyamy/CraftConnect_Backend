# class ArtisanUpdate(SQLModel):

#     address: str = Field(
#         title="address",
#         min_length=16,
#         max_length=250,
#         description="The address of the artisan.",
#     )


from pydantic import BaseModel, Field
from uuid import UUID

from pydantic_extra_types.phone_numbers import PhoneNumber


class ArtisanBase(BaseModel):

    phone_number: PhoneNumber | None = Field(
        title="phone number",
        description="The user's phone number.",
        examples=["+2349123456789"],
    )

    address: str = Field(
        title="address",
        min_length=16,
        max_length=250,
        description="The address of the artisan.",
    )

    pfp_url: str = Field(
        title="pfp url",
        description="The profile picture of the artisan.",
    )


class ArtisanCreate(ArtisanBase):
    pass


class ArtisanPublic(ArtisanBase):
    pass
