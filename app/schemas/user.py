from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator


class UserCreateSchema(BaseModel):
    login: str
    email: EmailStr
    password: str

    @field_validator("login")
    def validate_login(cls, value: str) -> str:
        if len(value) < 3 or len(value) > 20:
            raise ValueError("login should have at least 3 characters and at most 20")
        return value


class UserSchema(BaseModel):
    id: UUID
    login: str
    email: EmailStr
