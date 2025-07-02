from uuid import UUID
from app.shared import BaseHandler
from .tire_repository import TiresRepository
from .tire_schema import TiresBrandCreate, TiresBrandUpdate


class TiresHandler(BaseHandler):

    def __init__(self, repository: TiresRepository):
        super().__init__(repository)
        self.repository: TiresRepository = repository

    async def create_tire_brand(
        self,
        tire_brand_data: TiresBrandCreate,
    ):
        return await super().create_obj(data=tire_brand_data)

    async def update_tire_brand(
        self,
        tire_brand_id: UUID,
        tire_brand_data: TiresBrandUpdate,
    ):
        return await super().update_obj(id=tire_brand_id, data=tire_brand_data)

    async def delete_tire_brand(
        self,
        tire_brand_id: UUID,
    ):
        return await super().delete_obj(id=tire_brand_id)

    async def get_all_tires(
        self,
        query: str,
        cursor: int | None,
        take: int | None,
    ):
        return await super().get_all_obj_by_scroll(
            query=query,
            cursor=cursor,
            take=take,
        )

    async def get_tire_by_id(self, tire_brand_id: UUID):
        return await super().get_obj_by_id(id=tire_brand_id)

    async def get_tire_by_name(self, tire_brand_name: str):
        return await super().get_obj_by_name(name=tire_brand_name)
