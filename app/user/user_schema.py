from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str


class UserResponce(UserBase):
    id: int

    class Config:
        from_attributes = True
        validate_by_name = True
