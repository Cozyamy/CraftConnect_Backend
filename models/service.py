from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class ServiceLocation(str, Enum):

    USER = "USER"
    ARTISAN = "ARTISAN"


class ServiceBase(BaseModel):

    category_id: UUID | None = Field(default=None)

    name: str = Field(
        min_length=3,
        max_length=100,
        description="The name of the service.",
    )

    images: list[str] = Field(
        description="The service images.",
    )


class ServiceCreate(ServiceBase):

    artisan_id: UUID | None = Field(default=None)

    user_id: UUID | None = Field(default=None)

    price: float = Field(
        ge=550.0,
        description="The price of the service.",
    )

    description: str = Field(
        description="The service description.",
    )

    location: ServiceLocation = Field(
        description="The service location, either the users' or artisans'.",
    )
