from uuid import UUID
from pydantic import BaseModel


class DiscBrandCreate(BaseModel):
    name: str


class DiscBrandUpdate(DiscBrandCreate):
    pass


class DiscBrandResponse(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True
        validate_by_name = True
