import re

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.user import UserRole
from core.exceptions import BadRequestException


class RegisterUserRequest(BaseModel):
    email: EmailStr = Field(description="Email")
    first_name: str | None = Field(max_length=50, description="Firstname")
    last_name: str | None = Field(max_length=50, description="Lastname")
    role: UserRole | None = Field(description="User Role")
    activated: bool = Field(description="activated")
    password: str = Field(max_length=50, min_length=8, description="Password")

    @field_validator("password", mode="after")
    def validate_password(cls, value: str) -> str:
        password_pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
        if not password_pattern.match(value):
            raise BadRequestException(
                message="Password must contain at least 8 characters, including one uppercase letter, one lowercase letter, one number, and one special character."
            )
        return value
