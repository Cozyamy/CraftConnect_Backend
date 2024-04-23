from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4


class Services(table=True):
    pass


class Category(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)

    name: str = Field(
        title="name",
        min_length=3,
        max_length=100,
        description="The name of the category.",
        example="Photography",
    )

    services: list["Services"] = Relationship(back_populates="category")
