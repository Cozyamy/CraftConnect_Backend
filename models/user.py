import re
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import HTTPException
from pydantic import AfterValidator, EmailStr
from pydantic.dataclasses import dataclass
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import VARCHAR, Column, Field, SQLModel


def validate_password(value: str) -> str:
    """
    Validates the password value against a regex pattern to ensure it meets the expected criteria.

    Args:
    - `cls (class)`: The class object.
    - `value (str)`: The password value to be validated.

    Raises:
    - `HTTPException`: If the password value does not meet the expected criteria.

    Returns:
    - `str`: The validated password value.
    """

    regex_pattern: str = r"((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"

    if not re.match(regex_pattern, value):
        raise HTTPException(
            status_code=422,
            detail="password does not meet the expected criteria",
        )

    return value


class UserBase(SQLModel):
    name: str = Field(
        title="name",
        min_length=4,
        max_length=100,
        description="The full name of the user",
    )

    mail: EmailStr = Field(
        title="email",
        sa_column=Column(
            "email",
            VARCHAR,
            unique=True,
            index=True,
        ),
        description="The user's email address.",
    )

    phone: PhoneNumber = Field(
        title="phone number",
        description="The user's phone number.",
    )

    city: str = Field(
        title="address",
        description="the address of the user",
    )

    address: str


class UserCreate(UserBase, table=True):
    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=100,
            description="The user's password.",
        ),
        AfterValidator(validate_password),
    ]


class User(UserCreate, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)


