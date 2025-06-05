from uuid import UUID
from pydantic import BaseModel


class CarBrandBase(BaseModel):
    name: str


class CarBrandCreate(CarBrandBase):
    pass


class CarBrandCreateMessage(CarBrandCreate):
    picture: str


class CarBrandUpdate(CarBrandBase):
    pass


class CarBrandResponse(CarBrandBase):
    id: UUID
    picture: str

    class Config:
        from_attributes = True
        validate_by_name = True
