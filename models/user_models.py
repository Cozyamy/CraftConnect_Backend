from sqlmodel import SQLModel, Field, Relationship, Column, VARCHAR, ForeignKey
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import List, Optional
from datetime import datetime, timezone


class UserBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

class UserCreate(UserBase):
    email: EmailStr = Field(
        ...,
        sa_column=Column("email", VARCHAR, unique=True, index=True),
        description="Email of the user",
    )

class UserDetail(BaseModel):
    first_name: str = Field(min_length=3, max_length=50, description="Name of the User", schema_extra={'example': ["John"]}, title="First Name")
    last_name: str = Field(min_length=3, max_length=50, description="Last Name of User", schema_extra={'example': "Doe"}, title="Last Name")
    phone_number: Optional[str] = Field(default=None, description="Phone Number", schema_extra={'example': "+234823456789"}, title="Phone Number")

class User(UserCreate, table=True):
    __tablename__ = "users"
    password: str   
    first_name: str
    last_name: str
    phone_number: PhoneNumber | None
    is_premium: bool = Field(default=False)
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    artisan: Optional["Artisan"] = Relationship(back_populates="user")
    services: List["Service"] = Relationship(back_populates="user")


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

class Category(SQLModel, table=True):
    __tablename__ = "categories"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    services: List["Service"] = Relationship(back_populates="category")

class Artisan(SQLModel, table=True):
    __tablename__ = "artisans"
    id: Optional[int] = Field(default=None, primary_key=True)
    address: str
    picture_name: str
    user_id: Optional[int] = Field(
        foreign_key="users.id",
        description="ID of the user associated with this artisan profile",
    )
    user: Optional[User] = Relationship(back_populates="artisan")
    services: List["Service"] = Relationship(back_populates="artisan")

class ArtisanIn(SQLModel):
    address: str

class ServiceBase(SQLModel):
    price: float
    description: str
    location: str
    picture_1: str
    picture_2: Optional[str] = None

class ServiceCreate(ServiceBase):
    category_id: int
    user_id: int

class Service(ServiceBase, table=True):
    __tablename__ = "services"
    id: Optional[int] = Field(default=None, primary_key=True)
    category_id: int = Field(foreign_key="categories.id")
    artisan_id: int = Field(foreign_key="artisans.id")
    user_id: int = Field(foreign_key="users.id")
    category: "Category" = Relationship(back_populates="services")
    artisan: "Artisan" = Relationship(back_populates="services")
    user: "User" = Relationship(back_populates="services")