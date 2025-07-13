from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from app.car.product.product_schema import ProductResponseCompressed
from .order_enums import OrderStatuses


class OrderCreate(BaseModel):
    user_name: str
    user_phone: str
    description: str
    city_to_ship: str
    adress_to_ship: str
    postal_code: str


class OrderUpdate(OrderCreate):
    pass


class OrderFiltersCompressed(BaseModel):
    created_to: datetime | None = None
    created_from: datetime | None = None
    status: OrderStatuses | None = None


class OrderFilters(OrderFiltersCompressed):
    user_name: str | None = None
    user_phone: str | None = None
    city_to_ship: str | None = None
    adress_to_ship: str | None = None
    postal_code: str | None = None


class OrderResponse(OrderCreate):
    id: UUID
    user_id: UUID | None
    status: OrderStatuses

    class Config:
        from_attributes = True
        validate_by_name = True


class OrderItemResponse(BaseModel):
    products_count: int
    products: list[ProductResponseCompressed]


class OrderManualResponse(BaseModel):
    denied: list[str]
    order_data: OrderResponse
