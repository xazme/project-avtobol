import json
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, model_validator
from app.car.tire.tire import TireCreate, TireResponse, TireFilters
from app.car.disc.disc import DiscCreate, DiscResponse, DiscFilters
from app.car.engine import EngineCreate, EngineResponse, EngineFilters
from .product_enums import BodyType, Currency, ProductCondition, Availability
from ..engine.engine_enums import GearboxType, FuelType


class ProductCreate(BaseModel):
    OEM: str | None = None
    VIN: str | None = None
    car_brand_id: UUID
    car_series_id: UUID
    car_part_id: UUID
    year: int = 1980
    type_of_body: BodyType | None = None

    tire: TireCreate | None = None
    disc: DiscCreate | None = None
    engine: EngineCreate | None = None

    description: str
    price: float
    discount: float | None = None
    currency: Currency = Currency.USD
    condition: ProductCondition = ProductCondition.USED
    availability: Availability = Availability.IN_STOCK
    note: str | None = None
    count: int = 1

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class ProductUpdate(ProductCreate):
    pictures: list[str] | None = None


class ProductResponse(BaseModel):
    id: UUID
    article: str
    OEM: str | None
    VIN: str | None
    car_brand_id: UUID
    car_series_id: UUID
    car_part_id: UUID
    year: int
    type_of_body: BodyType | None
    tire: TireResponse | None = None
    disc: DiscResponse | None = None
    engine: EngineResponse | None = None
    description: str
    price: float
    discount: float | None
    currency: Currency
    condition: ProductCondition
    availability: Availability
    note: str | None = None
    count: int
    pictures: list[str]
    is_printed: bool
    is_available: bool
    created_at: datetime
    idriver_id: str | None
    allegro_id: str | None

    class Config:
        from_attributes = True
        validate_by_name = True


class ProductResponseExtend(BaseModel):
    id: UUID
    article: str
    OEM: str | None
    VIN: str | None
    pictures: list[str]

    car_brand_id: UUID | None = None
    car_brand_name: str
    car_series_id: UUID | None = None
    car_series_name: str
    car_part_id: UUID | None = None
    car_part_name: str

    year: int | None
    type_of_body: BodyType | None
    condition: ProductCondition

    engine: EngineResponse | None = None
    disc: DiscResponse | None = None
    tire: TireResponse | None = None

    description: str
    price: float
    discount: float | None
    currency: Currency
    note: str | None = None
    count: int
    availability: Availability
    is_printed: bool | None = None
    is_available: bool | None = None
    created_at: datetime | None = None
    post_by: UUID | None = None
    idriver_id: str | None
    allegro_id: str | None

    class Config:
        from_attributes = True
        validate_by_name = True


class ProductFilters(BaseModel):
    article: str | None = None
    car_brand_id: UUID | None = None
    car_series_id: UUID | None = None
    car_part_id: UUID | None = None
    price_from: float | None = None
    price_to: float | None = None
    year_from: int | None = None
    year_to: int | None = None
    type_of_body: BodyType | None = None
    condition: ProductCondition | None = None
    availability: Availability | None = None


class ProductFiltersExtended(ProductFilters):
    is_printed: bool | None = None
    is_available: bool | None = None
    created_from: datetime | None = None
    created_to: datetime | None = None
    post_by: UUID | None = None
