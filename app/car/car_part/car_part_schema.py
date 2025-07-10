from uuid import UUID
from pydantic import BaseModel


class CarPartBase(BaseModel):
    name: str


class CarPartCreate(CarPartBase):
    pass


class CarPartUpdate(CarPartBase):
    pass


class CarPartResponse(CarPartBase):
    id: UUID

    class Config:
        from_attributes = True
        validate_by_name = True
