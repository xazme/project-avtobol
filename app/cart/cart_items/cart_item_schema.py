from uuid import UUID
from pydantic import BaseModel


class CartAddItem(BaseModel):
    product_id: UUID


class CartDeleteItem(CartAddItem):
    product_id: UUID


class CartItemResponseExtended(BaseModel):
    id: UUID
    product_id: UUID
    article: str
    car_brand_name: str
    car_series_name: str
    car_part_type: str
    price: float
    discount: float

    class Config:
        from_attributes = True
        validate_by_name = True


class CartItemResponse(BaseModel):
    cart_id: UUID
    product_id: UUID

    class Config:
        from_attributes = True
        validate_by_name = True
