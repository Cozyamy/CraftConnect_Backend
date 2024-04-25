from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .service import Service


class CategoryCreate(SQLModel):

    name: str = Field(
        unique=True,
        index=True,
        title="name",
        min_length=3,
        max_length=100,
        description="The name of the category.",
        schema_extra={"examples": ["Photography"]},
    )

    services: List["Service"] = Relationship(back_populates="category")
