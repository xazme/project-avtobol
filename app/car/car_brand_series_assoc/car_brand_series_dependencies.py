from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .car_brand_series_model import CarBrandPartSeriesAssoc
from .car_brand_series_repository import CarBrandSeriesRepository
from .car_brand_series_handler import CarBrandSeriesHandler


def get_brand_series_handler(session: AsyncSession = Depends(DBService.get_session)):
    repository = CarBrandSeriesRepository(
        session=session,
        model=CarBrandPartSeriesAssoc,
    )
    return CarBrandSeriesHandler(repository=repository)
