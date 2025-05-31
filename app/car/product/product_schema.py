from uuid import UUID
from pydantic import BaseModel
from .product_enums import GearboxType, BodyType, FuelType, ProductCondition


class ProductBase(BaseModel):
    car_brand_id: UUID
    car_series_id: UUID
    car_part_id: UUID
    year: int
    volume: float
    gearbox: GearboxType | None = None
    fuel: FuelType | None = None
    type_of_body: BodyType | None = None
    condition: ProductCondition
    description: str
    real_price: float
    fake_price: float
    count: int


class ProductFilters(BaseModel):
    car_brand_id: UUID | None = None
    car_series_id: UUID | None = None
    car_part_id: UUID | None = None
    price_from: float | None = None
    price_to: float | None = None
    year_from: int | None = None
    year_to: int | None = None
    volume: float | None = None
    fuel: FuelType | None = None
    gearbox: GearboxType | None = None
    type_of_body: BodyType | None = None
    condition: ProductCondition


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductResponse(BaseModel):
    id: UUID
    pictures: list[str]
    car_brand_name: str
    car_series_name: str
    car_part_name: str
    year: int
    volume: float
    gearbox: GearboxType | None
    fuel: FuelType | None
    type_of_body: BodyType | None
    condition: ProductCondition
    description: str
    real_price: float
    fake_price: float
    count: int

    class Config:
        from_attributes = True
        validate_by_name = True
