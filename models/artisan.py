from uuid import UUID, uuid4

from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import Field, SQLModel


class ArtisanBase(SQLModel):
    pass


class ArtisanCreate(SQLModel):
    # phone_number
    pass


class Artisan(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, unique=True)

    phone_number: PhoneNumber | None = Field(
        title="phone number",
        description="The user's phone number.",
        schema_extra={"examples": ["+2349123456789"]},
    )
