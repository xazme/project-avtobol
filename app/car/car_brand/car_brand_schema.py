from uuid import UUID
from fastapi import Form
from pydantic import BaseModel


class CarBrandBase(BaseModel):
    name: str = Form(...)


class CarBrandCreate(CarBrandBase):
    pass


class CarBrandUpdate(CarBrandBase):
    pass


class CarBrandResponse(CarBrandBase):
    id: UUID
    picture: str

    class Config:
        from_attributes = True
        validate_by_name = True
