from typing import List
from uuid import UUID, uuid4
from datetime import datetime, timezone

from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import JSON, Column, Field, SQLModel, Relationship

from .user import UserCreate
from .artisan import ArtisanCreate


class User(UserCreate, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    pfp_url: str | None = Field(default=None)

    is_premium: bool = Field(default=False)
    is_artisan: bool = Field(default=False)

    # orders: List[str] = Field(default=[], sa_column=Column(JSON))
    # services: List[str] = Field(default=[], sa_column=Column(JSON))

    orders: list["Order"] = Relationship(back_populates="user")
    services: list["Service"] = Relationship(back_populates="user")

    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = Field(default=None)


class Artisan(ArtisanCreate, table=True):
    id: UUID | None = Field(default_factory=uuid4, unique=True, primary_key=True)


class Category(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)


class Service(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)


class Order(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
