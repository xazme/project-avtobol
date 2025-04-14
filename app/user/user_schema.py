from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., alias="obj_name")
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserResponce(BaseModel):
    id: int
    username: str = Field(..., alias="obj_name")

    class Config:
        from_attributes = True
        validate_by_name = True
