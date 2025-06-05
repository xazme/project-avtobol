from uuid import UUID
from fastapi import Form
from pydantic import BaseModel, Field


class CarBrandBase(BaseModel):
    name: str


class CarBrandCreate(CarBrandBase):
    pass


class CarBrandMessage(BaseModel):
    name: str = Field(...)
    picture: str = Field(...)


class CarBrandUpdate(CarBrandBase):
    pass


class CarBrandResponse(CarBrandBase):
    id: UUID
    picture: str

    class Config:
        from_attributes = True
        validate_by_name = True
