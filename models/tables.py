from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import JSON, Column, Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)

    first_name: str

    last_name: str

    email: str = Field(default=None, index=True, unique=True)

    phone_number: PhoneNumber | None = Field(default=None)

    pfp_url: str | None = Field(default=None)

    is_premium: bool = Field(default=False)

    is_artisan: bool = Field(default=False)

    artisan: Optional["Artisan"] = Relationship(back_populates="user")

    orders: list["Order"] = Relationship(back_populates="user")

    services: list["Service"] = Relationship(back_populates="user")

    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    updated_at: datetime | None = Field(default=None)

    # orders: List[str] = Field(default=[], sa_column=Column(JSON))
    # services: List[str] = Field(default=[], sa_column=Column(JSON))


class Artisan(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, unique=True, primary_key=True)

    user_id: UUID | None = Field(default=None, foreign_key="user.id")

    phone_number: PhoneNumber

    pfp_url: str

    address: str

    user: Optional["User"] = Relationship(back_populates="artisan")

    orders: list["Order"] = Relationship(back_populates="artisan")

    services: list["Service"] = Relationship(back_populates="artisan")


class Category(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)

    name: str = Field(unique=True, index=True)

    services: list["Service"] = Relationship(back_populates="category")


class Service(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)

    price: float

    description: str

    location: str

    images: List[str] = Field(default=[], sa_column=Column(JSON))

    user_id: UUID | None = Field(default=None, foreign_key="user.id")

    category_id: UUID | None = Field(default=None, foreign_key="category.id")

    artisan_id: UUID | None = Field(default=None, foreign_key="artisan.id")

    category: Optional["Category"] = Relationship(back_populates="service")

    artisan: Optional["Artisan"] = Relationship(back_populates="service")

    user: Optional["User"] = Relationship(back_populates="service")

    orders: List["Order"] = Relationship(back_populates="service")


class Order(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)

    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc()))

    user: Optional["User"] = Relationship(back_populates="order")

    artisan: Optional["Artisan"] = Relationship(back_populates="order")

    service: Optional["Service"] = Relationship(back_populates="order")

    user_id: UUID | None = Field(default=None, foreign_key="user.id")

    artisan_id: UUID | None = Field(default=None, foreign_key="artisan.id")

    service_id: UUID | None = Field(default=None, foreign_key="service.id")

    status: str
