from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from app.core import settings
from app.storage import get_storage_handler, StorageHandler
from .car_brand_model import CarBrand
from .car_brand_repository import CarBrandRepository
from .car_brand_handler import CarBrandHandler


def get_car_brand_handler(
    session: AsyncSession = Depends(DBService.get_session),
    storage: StorageHandler = Depends(get_storage_handler),
) -> CarBrandHandler:
    repository = CarBrandRepository(
        session=session,
        model=CarBrand,
    )
    return CarBrandHandler(repository=repository, storage=storage)
