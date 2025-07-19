import json
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, model_validator
from .product_enums import BodyType, Currency, ProductCondition, Availability
from ..tire.tire import TireCreate, TireResponse
from ..disc.disc import DiscCreate, DiscResponse
from ..engine import EngineCreate, EngineResponse


class ProductCreate(BaseModel):
    OEM: str | None = None
    VIN: str | None = None
    car_brand_id: UUID
    car_series_id: UUID
    car_part_id: UUID
    year: int = 1980
    type_of_body: BodyType | None = None
    details: TireCreate | DiscCreate | EngineCreate | None = None
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


class ProductResponseCompressed(BaseModel):
    id: UUID
    article: str
    car_brand_name: str
    car_series_name: str
    car_part_name: str
    price: float
    discount: float
    picture: str

    class Config:
        from_attributes = True
        validate_by_name = True


class ProductResponseBase(BaseModel):
    id: UUID
    article: str
    OEM: str | None = None
    VIN: str | None = None
    pictures: list[str]
    car_series_year: str
    car_part_name: str
    year: int | None = None
    details: TireResponse | DiscResponse | EngineResponse | None = None
    description: str
    price: float
    discount: float | None = None
    currency: Currency
    count: int
    availability: Availability

    class Config:
        from_attributes = True
        validate_by_name = True


class ProductResponsePublic(ProductResponseBase):
    car_brand_name: str
    car_series_name: str
    car_part_name_latin: str


class ProductResponsePrivate(ProductResponseBase):
    car_brand_id: UUID | None = None
    car_brand_name: str
    car_series_id: UUID | None = None
    car_series_name: str
    note: str | None = None
    car_part_id: UUID | None = None
    idriver_id: str | None = None
    allegro_id: str | None = None
    is_printed: bool | None = None
    is_available: bool | None = None
    created_at: datetime | None = None
    post_by: UUID | None = None


class ProductFiltersBase(BaseModel):
    article: str | None = None
    price_from: float | None = None
    price_to: float | None = None
    year_from: int | None = None
    year_to: int | None = None
    type_of_body: BodyType | None = None
    condition: ProductCondition | None = None
    availability: Availability | None = None


class ProductFiltersPublic(ProductFiltersBase):
    car_brand_name: str | None = None
    car_series_name: str | None = None
    car_part_name: str | None = None


class ProductFiltersPrivate(ProductFiltersBase):
    car_brand_id: UUID | None = None
    car_series_id: UUID | None = None
    car_part_id: UUID | None = None
    is_printed: bool | None = None
    is_available: bool | None = None
    created_from: datetime | None = None
    created_to: datetime | None = None
    post_by: UUID | None = None
