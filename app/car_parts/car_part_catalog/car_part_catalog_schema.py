from pydantic import BaseModel


class CarPartCatalogBase(BaseModel):
    name: str


class CarPartCatalogCreate(CarPartCatalogBase):
    pass


class CarPartCatalogUpdate(CarPartCatalogBase):
    pass


class CarPartCatalogResponse(CarPartCatalogBase):
    id: int

    class Config:
        from_attributes = True
        validate_by_name = True
