from datetime import datetime
from uuid import UUID
from fastapi import Form, Body
from pydantic import BaseModel
from app.shared import Diametr
from app.car.tire import Season, CarType
from .product_enums import (
    GearboxType,
    BodyType,
    FuelType,
    ProductCondition,
    Currency,
    Availability,
)


class ProductFilters(BaseModel):
    # Основные
    car_brand_id: UUID | None = None
    car_series_id: UUID | None = None
    car_part_id: UUID | None = None
    price_from: float | None = None
    price_to: float | None = None
    discount_from: float | None = None
    discount_to: float | None = None
    currency: Currency | None = None
    year_from: int | None = None
    year_to: int | None = None
    volume: float | None = None
    fuel: FuelType | None = None
    gearbox: GearboxType | None = None
    type_of_body: BodyType | None = None
    condition: ProductCondition | None = None
    availability: Availability | None = None

    # Диски
    disc_diametr: Diametr | None = None
    disc_width: float | None = None
    disc_ejection: float | None = None
    disc_dia: float | None = None
    disc_holes: int | None = None
    disc_pcd: float | None = None
    disc_brand_id: UUID | None = None
    disc_model: str | None = None

    # Шины
    tires_diametr: Diametr | None = None
    tires_width: float | None = None
    tires_height: float | None = None
    tires_index: str | None = None
    tires_car_type: CarType | None = None
    tires_brand_id: UUID | None = None
    tires_model: str | None = None
    tires_season: Season | None = None
    tires_residue_from: float | None = None
    tires_residue_to: float | None = None
    is_printed: bool | None = None
    is_available: bool | None = True
    created_from: datetime | None = None
    created_to: datetime | None = None


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

    # disc
    disc_diametr: Diametr | None = None
    disc_width: float | None = None
    disc_ejection: float | None = None
    disc_dia: float | None = None
    disc_holes: int | None = None
    disc_pcd: float | None = None
    disc_brand_id: UUID | None = None
    disc_model: str | None = None

    # tires
    tires_diametr: Diametr | None = None
    tires_width: float | None = None
    tires_height: float | None = None
    tires_index: str | None = None
    tires_car_type: CarType | None = None
    tire_brand_id: UUID | None = None
    tires_model: str | None = None
    tires_season: Season | None = None
    tires_residue: float | None = None

    description: str
    price: float
    discount: float | None = None
    currency: Currency = Currency.USD
    condition: ProductCondition = ProductCondition.USED
    availability: Availability = Availability.IN_STOCK
    note: str | None = None
    count: int = 1


class ProductUpdate(ProductCreate):
    pass


class ProductResponse(BaseModel):
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

    # disc
    disc_diametr: Diametr | None
    disc_width: float | None
    disc_ejection: float | None
    disc_dia: float | None
    disc_holes: int | None
    disc_pcd: float | None
    disc_brand_id: UUID | None
    disc_model: str | None

    # tires
    tires_diametr: Diametr | None
    tires_width: float | None
    tires_height: float | None
    tires_index: str | None
    tires_car_type: CarType | None
    tire_brand_id: UUID | None
    tires_model: str | None
    tires_season: Season | None
    tires_residue: float | None

    description: str
    price: float
    discount: float | None
    currency: Currency
    condition: ProductCondition
    availability: Availability
    note: str | None
    count: int = 1
    is_printed: bool
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True
        validate_by_name = True


class ProductResponseExtend(BaseModel):
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

    # Диск
    disc_diametr: Diametr | None
    disc_width: float | None
    disc_ejection: float | None
    disc_dia: float | None
    disc_holes: int | None
    disc_pcd: float | None
    disc_brand_name: str | None
    disc_model: str | None

    # Шины
    tires_diametr: Diametr | None
    tires_width: float | None
    tires_height: float | None
    tires_index: str | None
    tires_car_type: CarType | None
    tires_brand_name: str | None
    tires_model: str | None
    tires_season: Season | None
    tires_residue: float | None

    # Прочее
    description: str
    price: float
    discount: float | None
    currency: Currency
    note: str | None
    count: int
    availability: Availability
    is_printed: bool
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True
        validate_by_name = True
