from uuid import UUID
from pydantic import BaseModel


class CarBrandBase(BaseModel):
    name: str
    picture: str


class CarBrandCreate(CarBrandBase):
    pass


class CarBrandUpdate(CarBrandBase):
    pass


class CarBrandResponse(CarBrandBase):
    id: UUID

    class Config:
        from_attributes = True
        validate_by_name = True
