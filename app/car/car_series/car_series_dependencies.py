from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .car_series_service import CarSeriesService


def get_car_series_service(
    session: AsyncSession = Depends(DBService.get_session),
) -> CarSeriesService:
    return CarSeriesService(session=session)
