from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from .user_enums import UserRoles, UserStatuses


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    password: str
    phone_number: str


class UserUpdate(UserBase):
    password: str


class UserFilters(BaseModel):
    name: str | None = None
    phone_number: str | None = None
    status: UserStatuses | None = None
    role: UserRoles | None = None
    created_from: datetime | None = None
    created_to: datetime | None = None
    is_verified: bool | None = None


class UserResponse(UserBase):
    id: UUID
    status: UserStatuses
    role: UserRoles
    is_verified: bool

    class Config:
        from_attributes = True
        validate_by_name = True
