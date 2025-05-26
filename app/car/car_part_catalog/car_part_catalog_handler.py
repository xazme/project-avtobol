from uuid import UUID
from app.shared import BaseHandler
from .car_part_catalog_schema import CarPartCatalogCreate, CarPartCatalogUpdate


class CarPartCatalogHandler(BaseHandler):

    def __init__(self, repository):
        super().__init__(repository)

    async def create_part(
        self,
        data: CarPartCatalogCreate,
    ):
        return await super().create_obj(data)

    async def update_part(
        self,
        id: UUID,
        data: CarPartCatalogUpdate,
    ):
        return await super().update_obj(id, data)

    async def delete_part(
        self,
        id: UUID,
    ):
        return await super().delete_obj(id)

    async def get_part_by_id(
        self,
        id: UUID,
    ):
        return await super().get_obj_by_id(id)

    async def get_all_parts(self):
        return await super().get_all_obj()
