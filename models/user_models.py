from sqlmodel import SQLModel, Field, Relationship, Column, VARCHAR
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

class UserLogin(SQLModel):
    password: str = Field(min_length=8, max_length=100, description="Password of the user",title="Password")

class ArtisanCreate(BaseModel):
    category: str
    price: float
    location: str
    description: str

class CategoriesResponse(BaseModel):
    categories: List[str]

class ArtisanResponse(BaseModel):
    message: str

class ArtisanSearchResult(BaseModel):
    id: int
    category: str
    price: float
    location: str
    description: str
    created_at: datetime
    user_email: EmailStr
    user_first_name: str
    user_last_name: str
    user_phone_number: str
    pictures: List[str]

    class Config:
        from_attributes = True

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(SQLModel):
    sub: int | None = None

class UserOutput(SQLModel):
    id: int
    name: str
    email: EmailStr
    phone: PhoneNumber

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    artisan_id: int = Field(foreign_key="artisan.id")
    location: str
    work_details: str
    serial_number: str
    category: str
    date: datetime
    status: str = Field(default="pending")

class OrderDetails(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    artisan_id: int = Field(foreign_key="artisan.id")
    location: str
    work_details: str
    serial_number: str
    category: str
    date: datetime
    status: str = Field(default="pending")
    artisan: "Artisan" = Relationship(back_populates="orders")

class Artisan(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    category: str
    price: float
    location: str
    description: str
    pictures: List["Picture"] = Relationship(back_populates="artisan")
    created_at: datetime = Field(sa_column_kwargs={"default": datetime.now(timezone.utc)})
    user: "User" = Relationship(back_populates="artisans")
    orders: List[OrderDetails] | None = Relationship(back_populates="artisan")

class Picture(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    artisan_id: int = Field(foreign_key="artisan.id")
    path: str
    artisan: Artisan = Relationship(back_populates="pictures")

class User(UserCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    artisans: List[Artisan] | None = Relationship(back_populates="user")
    first_name: str
    last_name: str
    phone_number: Optional[str] = Field(default=None, description="Phone Number", schema_extra={'example': "+234823456789"}, title="Phone Number")


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None