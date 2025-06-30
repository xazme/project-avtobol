from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from .order_enums import OrderStatuses


class OrderCreate(BaseModel):
    article: str
    user_phone: str
    user_name: str
    description: str


class OrderCreatePrivate(BaseModel):
    articles: list[str]
    user_phone: str
    user_name: str
    description: str


class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID | None
    product_id: UUID
    order_group_id: UUID
    user_name: str | None
    user_phone: str | None
    description: str
    status: OrderStatuses

    class Config:
        from_attributes = True
        validate_by_name = True


class OrderResponseExtended(BaseModel):
    id: UUID
    user_id: UUID | None
    user_name: str
    user_phone: str
    product_id: UUID
    product_article: str
    product_brand: str
    product_series: str
    product_part: str
    created_at: datetime
    description: str
    status: OrderStatuses

    class Config:
        from_attributes = True
        validate_by_name = True
