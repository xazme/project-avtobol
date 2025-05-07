from pydantic import BaseModel


class CarBrandSeriesBase(BaseModel):
    brand_id: int
    car_part_id: int
    series_id: int
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


class CarBrandSeriesCreate(CarBrandSeriesBase):
    pass


class CarBrandSeriesUpdate(CarBrandSeriesBase):
    pass


class CarBrandSeriesResponce(BaseModel):
    id: int
    brand_id: int
    car_part_id: int
    series_id: int

    class Config:
        from_attributes = True
        validate_by_name = True
