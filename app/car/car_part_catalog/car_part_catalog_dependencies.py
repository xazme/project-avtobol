from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .car_part_catalog_repository import CarPartCatalogRepository
from .car_part_catalog_handler import CarPartCatalogHandler
from .car_part_catalog_model import CarPartCatalog


def get_car_part_catalog_handler(
    session: AsyncSession = Depends(DBService.get_session),
) -> CarPartCatalogHandler:
    car_part_repository = CarPartCatalogRepository(
        session=session,
        model=CarPartCatalog,
    )
    return CarPartCatalogHandler(repository=car_part_repository)
