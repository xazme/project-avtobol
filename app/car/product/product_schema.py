from uuid import UUID
from pydantic import BaseModel


class ProductBase(BaseModel):
    brand_id: UUID
    car_part_id: UUID
    series_id: UUID
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


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductResponce(ProductBase):
    id: UUID
    pictures: list = []

    class Config:
        from_attributes = True
        validate_by_name = True
