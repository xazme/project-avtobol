from uuid import UUID
from app.shared import BaseHandler
from .tires_repository import TiresRepository
from .tires_schema import TiresBrandCreate, TiresBrandUpdate


class TiresHandler(BaseHandler):

    def __init__(self, repository: TiresRepository):
        super().__init__(repository)
        self.repository: TiresRepository = repository

    async def create_tires_brand(
        self,
        data: TiresBrandCreate,
    ):
        return await super().create_obj(data=data)

    async def update_tires_brand(
        self,
        tires_brand_id: UUID,
        data: TiresBrandUpdate,
    ):
        return await super().update_obj(id=tires_brand_id, data=data)

    async def delete_tires_brand(
        self,
        tires_brand_id: UUID,
    ):
        return await super().delete_obj(id=tires_brand_id)

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

    async def get_tires_by_id(self, disc_brand_id: UUID):
        return await super().get_obj_by_id(id=disc_brand_id)

    async def get_tires_by_name(self, disc_brand_name: str):
        return await super().get_obj_by_name(name=disc_brand_name)
