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
    first_name: str = Field(
        title="name",
        min_length=3,
        max_length=100,
        description="The first name of the user.",
        schema_extra={
            "examples": ["John"],
        },
    )

    last_name: str = Field(
        title="name",
        min_length=3,
        max_length=100,
        description="The last name of the user.",
        schema_extra={
            "examples": ["Doe"],
        },
    )

    email: EmailStr = Field(
        title="email",
        sa_column=Column(
            "email",
            VARCHAR,
            unique=True,
            index=True,
        ),
        description="The user's email address.",
    )

    phone_number: PhoneNumber = Field(
        title="phone number",
        description="The user's phone number.",
        schema_extra={"examples": ["+2349123456789"]},
    )


class UserCreate(UserBase):
    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=100,
            description="The user's password must:\n"
            "- Contain at least one digit `(0-9)`.\n"
            "- Contain at least one lowercase letter `(a-z)`.\n"
            "- Contain at least one uppercase letter `(A-Z)`.\n"
            "- Contain at least one special character `(e.g., !@#$%^&*()_+-=[]{}|;':\",.<>?/)`.\n"
            "- Be between `8` and `64` characters in length.",
            schema_extra={"examples": ["Qwertyuiop123!"]},
        ),
        AfterValidator(validate_password),
    ]


class User(UserCreate, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
