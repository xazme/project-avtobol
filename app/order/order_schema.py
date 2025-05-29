from enum import Enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class OrderCreate(BaseModel):
    description: str
    status: Enum = None
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
    status: Enum

    class Config:
        from_attributes = True
        validate_by_name = True
