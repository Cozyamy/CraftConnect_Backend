from datetime import datetime, timezone

from pydantic import BaseModel, EmailStr, Field

from .artisan import ArtisanBase


class UserBase(BaseModel):

    first_name: str = Field(
        title="name",
        min_length=3,
        max_length=100,
        description="The first name of the user.",
        examples=["John"],
    )

    last_name: str = Field(
        title="name",
        min_length=3,
        max_length=100,
        description="The last name of the user.",
        examples=["Doe"],
    )

    email: EmailStr = Field(
        title="email",
        description="The user's email address.",
    )


class UserCreate(UserBase):

    phone_number: str | None = Field(
        default=None,
        title="phone number",
        description="The user's phone number.",
        examples=["+2349123456789"],
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


class UserUpdate(BaseModel):

    first_name: str | None = Field(
        default=None,
        title="name",
        min_length=3,
        max_length=100,
        description="The first name of the user.",
        examples=["John"],
    )

    last_name: str | None = Field(
        default=None,
        title="name",
        min_length=3,
        max_length=100,
        description="The last name of the user.",
        examples=["Doe"],
    )

    phone_number: str | None = Field(
        default=None,
        title="phone number",
        description="The user's phone number.",
        examples=["+2349123456789"],
    )

    pfp_url: str | None = Field(
        default=None,
        title="profile picture",
        description="The user's profile picture.",
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )


class UserPublic(UserBase):
    artisan: ArtisanBase | None = None
