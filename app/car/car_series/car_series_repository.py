from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from .car_series_model import CarSeries


class CarSeriesRepository(BaseCRUD):

    def __init__(
        self,
        session: AsyncSession,
        model: CarSeries,
    ):
        super().__init__(session, model)
