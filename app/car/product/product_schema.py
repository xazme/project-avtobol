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


class ProductUpdate(BaseModel):

    @classmethod
    def as_form(
        cls,
        OEM: str | None = Form(None),
        car_brand_id: UUID = Form(...),
        car_series_id: UUID = Form(...),
        car_part_id: UUID = Form(...),
        year: int = Form(default=1885, gt=1884, lt=2077),
        type_of_body: BodyType | None = Form(None),
        volume: float = Form(gt=0),
        gearbox: GearboxType | None = Form(None),
        fuel: FuelType | None = Form(None),
        engine_type: str | None = Form(None),
        VIN: str | None = Form(None),
        pictures: list[str] = Form(...),
        note: str = Form(...),
        description: str = Form(min_length=5, max_length=500),
        real_price: float = Form(gt=0),
        fake_price: float = Form(ge=0),
        condition: ProductCondition = Form(...),
        count: int = Form(default=1, ge=1),
    ):
        return cls(
            OEM=OEM,
            car_brand_id=car_brand_id,
            car_series_id=car_series_id,
            car_part_id=car_part_id,
            year=year,
            type_of_body=type_of_body,
            volume=volume,
            gearbox=gearbox,
            fuel=fuel,
            engine_type=engine_type,
            VIN=VIN,
            pictures=pictures,
            note=note,
            description=description,
            real_price=real_price,
            fake_price=fake_price,
            condition=condition,
            count=count,
        )


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
