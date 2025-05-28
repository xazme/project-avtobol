from uuid import UUID
from pydantic import BaseModel


class CarSeriesBase(BaseModel):
    name: str
    year: str


class CarSeriesCreate(CarSeriesBase):
    brand_id: UUID


class CarSeriesUpdate(CarSeriesBase):
    pass


class CarSeriesResponse(CarSeriesBase):
    id: UUID
    brand_id: UUID

    class Config:
        from_attributes = True
        validate_by_name = True
