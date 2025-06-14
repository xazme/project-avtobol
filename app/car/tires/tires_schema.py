from uuid import UUID
from pydantic import BaseModel


class TiresBase(BaseModel):
    name: str


class TiresBrandCreate(TiresBase):
    pass


class TiresBrandUpdate(TiresBase):
    pass


class TiresBrandResponse(TiresBase):
    id: UUID

    class Config:
        from_attributes = True
        validate_by_name = True
