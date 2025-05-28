from uuid import UUID
from app.shared import BaseHandler, ExceptionRaiser
from .car_series_repository import CarSeriesRepository
from .car_series_schema import CarSeriesCreate, CarSeriesUpdate


class CarSeriesHandler(BaseHandler):

    def __init__(
        self,
        repository: CarSeriesRepository,
    ):
        super().__init__(repository)
        self.repository = repository

    async def create_series(
        self,
        data: CarSeriesCreate,
    ):
        return await super().create_obj(data=data)

    async def update_series(
        self,
        series_id: UUID,
        data: CarSeriesUpdate,
    ):
        return await super().update_obj(id=series_id, data=data)

    async def delete_series(
        self,
        series_id: UUID,
    ):
        return await super().delete_obj(id=series_id)

    async def get_series_by_id(
        self,
        series_id: UUID,
    ):
        return await super().get_obj_by_id(id=series_id)

    async def get_all_series_obj(self):
        return await super().get_all_obj()

    async def check_relation(
        self,
        brand_id: UUID,
        series_id: UUID,
    ):
        result = await self.repository.check_relation(
            brand_id=brand_id,
            series_id=series_id,
        )

        if result is False:
            ExceptionRaiser.raise_exception(
                status_code=404, detail="Series does not belong to brand"
            )
        return result
