from sqlalchemy.ext.asyncio import AsyncSession
from .car_series_model import CarSeries
from app.shared import CRUDGenerator


class CarSeriesService(CRUDGenerator):

    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=CarSeries,
        )
