from sqlalchemy.ext.asyncio import AsyncSession
from .car_series_model import CarSeries
from app.shared import CRUDGenerator


class CarSeriesService(CRUDGenerator[CarSeries]):

    def __init__(self, session: AsyncSession, model: type[CarSeries]):
        super().__init__(session, model)
