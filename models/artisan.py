from uuid import UUID, uuid4

from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import Field, SQLModel


class ArtisanBase(SQLModel):
    pass


class ArtisanCreate(SQLModel):
    # phone_number
    pass


class ArtisanUpdate(SQLModel):
    address: str = Field(
        title="address",
        min_length=16,
        max_length=250,
        description="The address of the artisan.",
    )


class Artisan(SQLModel, table=True):
    id: UUID | None = Field(
        default_factory=uuid4,
        unique=True,
        primary_key=True,
    )

    phone_number: PhoneNumber | None = Field(
        title="phone number",
        description="The user's phone number.",
        schema_extra={"examples": ["+2349123456789"]},
    )
