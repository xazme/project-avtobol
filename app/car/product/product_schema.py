from datetime import datetime
from uuid import UUID
from fastapi import Form, Body
from pydantic import BaseModel
from .product_enums import GearboxType, BodyType, FuelType, ProductCondition


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
    condition: ProductCondition | None = None
    is_available: bool | None = None
    is_printed: bool | None = None


class ProductCreate(BaseModel):
    OEM: str | None
    car_brand_id: UUID
    car_series_id: UUID
    car_part_id: UUID
    year: int = 1885
    type_of_body: BodyType | None = None
    volume: float
    gearbox: GearboxType | None = None
    fuel: FuelType | None = None
    engine_type: str | None = None
    VIN: str | None = None
    pictures: list[str]
    note: str
    description: str
    real_price: float
    fake_price: float | None = None
    condition: ProductCondition
    count: int = 1


class ProductUpdate(ProductCreate):
    pass


class ProductResponseForWorker(BaseModel):
    OEM: str | None
    car_brand_id: UUID
    car_series_id: UUID
    car_part_id: UUID
    year: int
    type_of_body: BodyType | None
    volume: float
    gearbox: GearboxType | None
    fuel: FuelType | None
    engine_type: str | None
    VIN: str | None
    pictures: list[str]
    note: str
    description: str
    real_price: float
    fake_price: float | None
    condition: ProductCondition
    count: int

    class Config:
        from_attributes = True
        validate_by_name = True


class ProductResponse(BaseModel):
    id: UUID
    OEM: str | None
    VIN: str | None
    pictures: list[str]
    car_brand_name: str
    car_series_name: str
    car_part_name: str
    year: int | None
    volume: float | None
    gearbox: GearboxType | None
    fuel: FuelType | None
    type_of_body: BodyType | None
    condition: ProductCondition
    description: str
    note: str | None
    real_price: float
    fake_price: float | None
    count: int
    is_available: bool
    is_printed: bool
    created_at: datetime

    class Config:
        from_attributes = True
        validate_by_name = True
