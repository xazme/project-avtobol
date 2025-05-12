# from pydantic import BaseModel, EmailStr, Field


# class UserBase(BaseModel):
#     name: str
#     email: EmailStr
#     password: str


# class UserCreate(UserBase):
#     pass


# class UserUpdate(UserBase):
#     pass


# class UserResponce(BaseModel):
#     id: int

#     class Config:
#         from_attributes = True
#         validate_by_name = True
