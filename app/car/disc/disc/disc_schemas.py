from uuid import UUID
from pydantic import BaseModel
from app.car.shared import Diametr


class DiscCreate(BaseModel):
    disc_brand_id: UUID
    diametr: Diametr | None = None
    width: float | None = None
    ejection: float | None = None
    dia: float | None = None
    holes: int | None = None
    pcd: float | None = None
    model: str | None = None


class DiscUpdate(DiscCreate):
    pass


class DiscResponse(DiscCreate):
    id: UUID
    disc_brand_id: UUID
    diametr: Diametr | None
    width: float | None
    ejection: float | None
    dia: float | None
    holes: int | None
    pcd: float | None
    model: str | None

    class Config:
        from_attributes = True
        validate_by_name = True


class DiscFilters(BaseModel):
    diametr: Diametr | None = None
    width: float | None = None
    ejection: float | None = None
    dia: float | None = None
    holes: int | None = None
    pcd: float | None = None
    brand_id: UUID | None = None
    model: str | None = None
