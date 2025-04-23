from pydantic import BaseModel


class CarPartBase(BaseModel):
    id: str
    brand_id: str
    part_id: str
    series_id: str
    year: int
    type_of_body: str
    volume: float
    gearbox: str
    fuel: str
    type_of_engine: str
    VIN: int
    oem: int
    note: str
    description: str
    real_price: float
    fake_price: float
    count: int
    condition: str


class CarPartCreate(CarPartBase):
    pass


class CarPartUpdate(CarPartBase):
    pass


class CarPartResponce(BaseModel):
    pass
