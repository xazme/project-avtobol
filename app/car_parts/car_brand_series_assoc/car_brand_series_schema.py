import uuid
from pydantic import BaseModel


class CarPartBase(BaseModel):
    brand_id: uuid.UUID
    part_id: str  # uuid.UUID
    series_id: uuid.UUID
    # year: int
    # type_of_body: str
    # volume: float
    # gearbox: str
    # fuel: str
    # type_of_engine: str
    # VIN: int
    # oem: int
    # note: str
    # description: str
    # real_price: float
    # fake_price: float
    # count: int
    # condition: str


class CarPartCreate(CarPartBase):
    pass


class CarPartUpdate(CarPartBase):
    pass


class CarPartResponce(BaseModel):
    pass
