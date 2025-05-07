from fastapi import Form
from pydantic import BaseModel


class CarBrandBase(BaseModel):
    name: str = Form(...)
    picture: str = Form(...)


class CarBrandCreate(CarBrandBase):
    pass


class CarBrandUpdate(CarBrandBase):
    pass


class CarBrandResponse(CarBrandBase):
    id: int

    class Config:
        from_attributes = True
        validate_by_name = True
