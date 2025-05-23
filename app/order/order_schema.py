from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    created_at: datetime
    description: str
    status: Enum = None

    # COUNTRY CITY POSTCODE
    class Config:
        from_attributes = True
        validate_by_name = True


class OrderResponse(BaseModel):
    user_id: int
    product_id: int
    created_at: datetime
    description: str
    status: Enum

    class Config:
        from_attributes = True
        validate_by_name = True
