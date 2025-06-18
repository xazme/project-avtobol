from uuid import UUID
from pydantic import BaseModel


class CartBase(BaseModel):
    product_id: UUID


class CartCreate(CartBase):
    user_id: UUID


class CartResponse(CartBase):
    user_id: UUID
    product_id: UUID

    class Config:
        from_attributes = True
        validate_by_name = True


class CartResponseExtended(CartBase):
    user_id: UUID
    product_id: UUID
    product_brand: str
    product_series: str
    product_part: str

    class Config:
        from_attributes = True
        validate_by_name = True
