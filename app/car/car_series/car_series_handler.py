from typing import Optional
from uuid import UUID
from app.shared import BaseHandler, ExceptionRaiser
from .car_series_repository import CarSeriesRepository
from .car_series_schema import CarSeriesCreate, CarSeriesUpdate
from .car_series_model import CarSeries


class CarSeriesHandler(BaseHandler):

    def __init__(self, repository: CarSeriesRepository):
        super().__init__(repository)
        self.repository: CarSeriesRepository = repository

    async def create_series(
        self,
        data: CarSeriesCreate,
    ) -> Optional[CarSeries]:
        series: CarSeries | None = await self.create_obj(data=data)
        if not series:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Неудалось создать серию.",
            )
        return series

    async def update_series(
        self,
        car_series_id: UUID,
        data: CarSeriesUpdate,
    ) -> CarSeries:
        series: CarSeries | None = await self.update_obj(id=car_series_id, data=data)
        if not series:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Серия не найдена.",
            )
        return series

    async def delete_series(
        self,
        car_series_id: UUID,
    ) -> bool:
        result: bool = await self.delete_obj(id=car_series_id)
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Неудалось удалить серию.",
            )
        return result

    async def get_series_by_id(
        self,
        series_id: UUID,
    ) -> CarSeries:
        series: CarSeries | None = await self.get_obj_by_id(id=series_id)
        if not series:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Серия не найдена.",
            )
        return series

    async def get_all_series_obj(
        self,
    ) -> list[CarSeries]:
        return await self.get_all_obj()

    async def get_series_by_car_brand_id(
        self,
        car_brand_id: UUID,
    ) -> list[CarSeries]:
        return await self.repository.get_series_by_car_brand_id(
            car_brand_id=car_brand_id
        )

    async def get_all_series_by_scroll(
        self,
        query: str,
        cursor: int | None,
        take: int | None,
        car_brand_id: UUID,
    ):
        return await self.repository.get_all_series_by_scroll_and_brand_id(
            query=query,
            cursor=cursor,
            take=take,
            car_brand_id=car_brand_id,
        )

    async def check_relation(
        self,
        car_brand_id: UUID,
        car_series_id: UUID,
    ) -> bool:
        result: bool = await self.repository.check_relation(
            car_brand_id=car_brand_id,
            car_series_id=car_series_id,
        )
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Серия не принадлежит бренду.",
            )
        return result
