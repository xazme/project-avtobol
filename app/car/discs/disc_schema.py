from uuid import UUID
from pydantic import BaseModel


class DiscBase(BaseModel):
    name: str


class DiscBrandCreate(DiscBase):
    pass


class DiscBrandUpdate(DiscBase):
    pass


class DiscBrandResponse(DiscBase):
    id: UUID

    class Config:
        from_attributes = True
        validate_by_name = True
