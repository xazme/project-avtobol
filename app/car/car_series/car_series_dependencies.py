from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .car_series_model import CarSeries
from .car_series_handler import CarSeriesHandler
from .car_series_repository import CarSeriesRepository


def get_car_series_handler(
    session: AsyncSession = Depends(DBService.get_session),
) -> CarSeriesHandler:
    repository = CarSeriesRepository(session=session, model=CarSeries)
    return CarSeriesHandler(repository=repository)
