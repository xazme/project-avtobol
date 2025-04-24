import uuid
from pydantic import BaseModel


class CarSeriesBase(BaseModel):
    name: str
    year: str


class CarSeriesCreate(CarSeriesBase):
    brand_id: uuid.UUID


class CarSeriesUpdate(CarSeriesBase):
    pass


class CarSeriesResponse(CarSeriesBase):
    id: uuid.UUID
    brand_id: uuid.UUID

    class Config:
        from_attributes = True
        validate_by_name = True
