import uuid
from pydantic import BaseModel


class CarBrandBase(BaseModel):
    name: str
    url: str


class CarBrandCreate(CarBrandBase):
    pass


class CarBrandUpdate(CarBrandBase):
    pass


class CarBrandResponse(CarBrandBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
        validate_by_name = True
