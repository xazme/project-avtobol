from uuid import UUID
from pydantic import BaseModel, Field


class CarBrandBase(BaseModel):
    name: str


class CarBrandCreate(CarBrandBase):
    pass


class CarBrandUpdate(CarBrandBase):
    pass


class CarBrandCreateMessage(BaseModel):
    car_brand_data: dict
    file: str | None


class CarBrandUpdateMessage(BaseModel):
    car_brand_id: UUID
    car_brand_data: dict
    file: str | None


class CarBrandResponse(CarBrandBase):
    id: UUID
    picture: str

    class Config:
        from_attributes = True
        validate_by_name = True
