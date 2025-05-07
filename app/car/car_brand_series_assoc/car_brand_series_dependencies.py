from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .car_brand_series_service import CarBrandSeriesService
from .car_brand_series_model import CarBrandPartSeriesAssoc


def get_car_part_service(session: AsyncSession = Depends(DBService.get_session)):
    return CarBrandSeriesService(session=session)
