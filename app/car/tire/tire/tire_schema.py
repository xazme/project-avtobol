from uuid import UUID
from pydantic import BaseModel
from app.car.shared import Diametr
from .tire_enums import CarType, Season


class TireCreate(BaseModel):
    tire_brand_id: UUID
    diametr: Diametr | None = None
    width: float | None = None
    height: float | None = None
    index: str | None = None
    car_type: CarType | None = None
    model: str | None = None
    season: Season | None = None
    residue: float | None = None


class TireUpdate(TireCreate):
    pass


class TireResponse(BaseModel):
    id: UUID
    tire_brand_id: UUID
    diametr: Diametr | None
    width: float | None
    height: float | None
    index: str | None
    car_type: CarType | None
    model: str | None
    season: Season | None
    residue: float | None

    class Config:
        from_attributes = True
        validate_by_name = True


class TireFiltersBase(BaseModel):
    model: str | None = None
    season: Season | None = None
    residue_from: float | None = None
    residue_to: float | None = None
    diametr: Diametr | None = None
    width: float | None = None
    height: float | None = None
    index: str | None = None
    car_type: CarType | None = None


class TireFiltersPublic(TireFiltersBase):
    tire_brand_name: str | None = None


class TireFiltersPrivate(TireFiltersBase):
    tire_brand_id: UUID | None = None
