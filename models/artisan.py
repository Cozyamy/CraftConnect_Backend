from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .tables import Order, Service, User


class ArtisanBase(SQLModel):

    user: Optional["User"] = Relationship(back_populates="artisan")
    user_id: UUID | None = Field(default=None, foreign_key="user.id")
    services: List["Service"] = Relationship(back_populates="artisan")
    orders: List["Order"] = Relationship(back_populates="artisan")


class ArtisanCreate(ArtisanBase):

    phone_number: PhoneNumber | None = Field(
        title="phone number",
        description="The user's phone number.",
        schema_extra={"examples": ["+2349123456789"]},
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


class ArtisanUpdate(SQLModel):

    address: str = Field(
        title="address",
        min_length=16,
        max_length=250,
        description="The address of the artisan.",
    )
