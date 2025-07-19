from uuid import UUID
from pydantic import BaseModel


class TireBrandCreate(BaseModel):
    name: str


class TireBrandUpdate(TireBrandCreate):
    pass


class TireBrandResponse(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True
        validate_by_name = True
