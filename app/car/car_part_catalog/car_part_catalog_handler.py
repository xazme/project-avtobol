from typing import Optional
from uuid import UUID
from app.shared import BaseHandler, ExceptionRaiser
from .car_part_catalog_repository import CarPartRepository
from .car_part_catalog_model import CarPart
from .car_part_catalog_schema import CarPartCreate, CarPartUpdate


class CarPartHandler(BaseHandler):

    def __init__(self, repository: CarPartRepository):
        super().__init__(repository)
        self.repository: CarPartRepository = repository

    async def create_part(
        self,
        data: CarPartCreate,
    ) -> Optional[CarPart]:
        part: CarPart | None = await self.create_obj(data)
        if not part:
            ExceptionRaiser.raise_exception(
                status_code=400, detail="Failed to create car part."
            )
        return part

    async def update_part(
        self,
        car_part_id: UUID,
        data: CarPartUpdate,
    ) -> Optional[CarPart]:
        part: CarPart | None = await self.update_obj(id=car_part_id, data=data)
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
    ) -> Optional[CarPart]:
        part: CarPart | None = await self.get_obj_by_id(id=car_part_id)
        if not part:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Car part not found.",
            )
        return part

    async def get_all_parts(
        self,
        query: str,
        cursor: int,
        take: int,
    ) -> tuple[int | None, list]:
        return await self.get_all_obj_by_scroll(
            query=query,
            cursor=cursor,
            take=take,
        )
