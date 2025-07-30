from uuid import UUID
from pydantic import BaseModel


class CartCreate(BaseModel):
    user_id: UUID


class CartResponse(CartCreate):
    id: UUID

    class Config:
        from_attributes = True
        validate_by_name = True
