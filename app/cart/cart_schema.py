from pydantic import BaseModel


class CartBase(BaseModel):
    user_id: int
    product_id: int


class CartCreate(CartBase):
    user_id: int
    product_id: int


class CartResponse(CartBase):
    user_id: int
    product_id: int

    class Config:
        from_attributes = True
        validate_by_name = True
