from typing import Optional
from uuid import UUID, uuid4

from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import VARCHAR, Column, Field, SQLModel


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


class UserCreate(UserBase):
    phone_number: str | None = Field(
        default=None,
        title="phone number",
        description="The user's phone number.",
        schema_extra={"examples": ["+2349123456789"]},
    )

    #     password: Optional[
    #         Annotated[
    #             str,
    #             Field(
    #                 min_length=8,
    #                 max_length=100,
    #                 description="The user's password must:\n"
    #                 "- Contain at least one digit `(0-9)`.\n"
    #                 "- Contain at least one lowercase letter `(a-z)`.\n"
    #                 "- Contain at least one uppercase letter `(A-Z)`.\n"
    #                 "- Contain at least one special character `(e.g., !@#$%^&*()_+-=[]{}|;':\",.<>?/)`.\n"
    #                 "- Be between `8` and `64` characters in length.",
    #                 schema_extra={"examples": ["Qwertyuiop123!"]},
    #             ),
    #             AfterValidator(validate_password),
    #         ]
    #     ] = None


class User(UserCreate, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)

    # is_artisan: bool = Field(default=False)
