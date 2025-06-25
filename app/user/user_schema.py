from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    phone_number: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str


class UserResponse(UserBase):
    id: UUID

    class Config:
        from_attributes = True
        validate_by_name = True
