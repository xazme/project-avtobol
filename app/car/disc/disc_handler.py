from uuid import UUID
from app.shared import BaseHandler
from .disc_repository import DiscRepository
from .disc_schema import DiscBrandCreate, DiscBrandUpdate


class DiscHandler(BaseHandler):

    def __init__(self, repository: DiscRepository):
        super().__init__(repository)
        self.repository: DiscRepository = repository

    async def create_disc_brand(
        self,
        disc_brand_data: DiscBrandCreate,
    ):
        return await super().create_obj(data=disc_brand_data)

    async def update_disc_brand(
        self,
        disc_brand_id: UUID,
        disc_brand_data: DiscBrandUpdate,
    ):
        return await super().update_obj(id=disc_brand_id, data=disc_brand_data)

    async def delete_disc_brand(
        self,
        disc_brand_id: UUID,
    ):
        return await super().delete_obj(id=disc_brand_id)

    async def get_all_discs(
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

    async def get_disc_by_id(self, disc_brand_id: UUID):
        return await super().get_obj_by_id(id=disc_brand_id)

    async def get_disc_by_name(self, disc_brand_name: str):
        return await super().get_obj_by_name(name=disc_brand_name)
