from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from app.storage import storage_service
from app.core import settings
from .car_brand_model import CarBrand
from .car_brand_repository import CarBrandRepository
from .car_brand_handler import CarSeriesHandler


def get_car_brand_handler(
    session: AsyncSession = Depends(DBService.get_session),
) -> CarSeriesHandler:
    repository = CarBrandRepository(
        session=session,
        model=CarBrand,
    )
    return CarSeriesHandler(repository=repository, storage=storage_service)
