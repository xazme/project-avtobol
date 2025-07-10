from uuid import UUID
from pydantic import BaseModel
from .engine_enums import GearboxType, FuelType


class EngineCreate(BaseModel):
    product_id: UUID
    engine_type: str | None = None
    gearbox: GearboxType | None = None
    fuel: FuelType | None = None
    volume: float | None = None


class EngineUpdate(EngineCreate):
    pass


class EngineResponse(BaseModel):
    id: UUID
    product_id: UUID
    engine_type: str | None
    gearbox: GearboxType | None
    fuel: FuelType | None
    volume: float | None

    class Config:
        from_attributes = True
        validate_by_name = True


class EngineFilters(BaseModel):
    gearbox: GearboxType | None = None
    fuel: FuelType | None = None
    volume: float | None = None
    engine_type: str | None = None
