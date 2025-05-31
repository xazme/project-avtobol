from typing import Optional
from uuid import UUID
from app.shared import BaseHandler, ExceptionRaiser
from .car_part_catalog_repository import CarPartCatalogRepository
from .car_part_catalog_model import CarPartCatalog
from .car_part_catalog_schema import CarPartCatalogCreate, CarPartCatalogUpdate


class CarPartCatalogHandler(BaseHandler):

    def __init__(self, repository: CarPartCatalogRepository):
        super().__init__(repository)
        self.repository: CarPartCatalogRepository = repository

    async def create_part(
        self,
        data: CarPartCatalogCreate,
    ) -> Optional[CarPartCatalog]:
        part: CarPartCatalog | None = await self.create_obj(data)
        if not part:
            ExceptionRaiser.raise_exception(
                status_code=400, detail="Failed to create car part."
            )
        return part

    async def update_part(
        self,
        car_part_id: UUID,
        data: CarPartCatalogUpdate,
    ) -> CarPartCatalog:
        part: CarPartCatalog | None = await self.update_obj(id=car_part_id, data=data)
        if not part:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Car part not found.",
            )
        return part

    async def delete_part(
        self,
        car_part_id: UUID,
    ) -> bool:
        result: bool = await self.delete_obj(id=car_part_id)
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Failed to delete car part.",
            )
        return result

    async def get_part_by_id(
        self,
        car_part_id: UUID,
    ) -> CarPartCatalog:
        part: CarPartCatalog | None = await self.get_obj_by_id(id=car_part_id)
        if not part:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Car part not found.",
            )
        return part

    async def get_all_parts(
        self,
    ) -> list[CarPartCatalog]:
        return await self.get_all_obj()
