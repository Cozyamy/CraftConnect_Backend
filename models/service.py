from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .artisan import Artisan
    from .tables import Service


class ServiceLocation(str, Enum):
    USER = "USER"
    ARTISAN = "ARTISAN"


class ServiceBase(SQLModel):
    category_id: UUID = Field(foreign_key="category.id")

    name: str = Field(
        min_length=3,
        max_length=100,
        description="The name of the service",
    )


class ServiceCreate(SQLModel):
    user_id: UUID = Field(foreign_key="user.id")

    price: float = Field(
        ge=0.0,
        description="The price of the service",
    )

    description: str = Field(description="")

    location: ServiceLocation = Field(description="")

    images: list[str] = Field()

    pass
