from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from .order_enums import OrderStatuses


class OrderCreate(BaseModel):
    description: str
    status: OrderStatuses | None = None
    # COUNTRY CITY POSTCODE


class OrderResponse(BaseModel):
    user_id: UUID
    user_name: str
    user_phone: str
    product_id: UUID
    product_brand: str
    product_series: str
    product_part: str
    created_at: datetime
    description: str
    status: OrderStatuses

    class Config:
        from_attributes = True
        validate_by_name = True
