from pydantic import BaseModel


class CarSeriesBase(BaseModel):
    name: str
    year: str


class CarSeriesCreate(CarSeriesBase):
    brand_id: int


class CarSeriesUpdate(CarSeriesBase):
    pass


class CarSeriesResponse(CarSeriesBase):
    id: int
    brand_id: int

    class Config:
        from_attributes = True
        validate_by_name = True
