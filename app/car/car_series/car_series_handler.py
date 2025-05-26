from uuid import UUID
from app.shared import BaseHandler
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
        return super().create_obj(data)

    async def update_series(
        self,
        id: UUID,
        data: CarSeriesUpdate,
    ):
        return super().update_obj(id, data)

    def delete_series(
        self,
        id: UUID,
    ):
        return super().delete_obj(id)

    def get_series_by_id(
        self,
        id: UUID,
    ):
        return super().get_obj_by_id(id)

    def get_all_series_obj(self):
        return super().get_all_obj()
