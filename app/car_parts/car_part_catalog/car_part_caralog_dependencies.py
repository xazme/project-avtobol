from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .car_part_catalog_service import CarPartCatalogService
from .car_part_catalog_model import CarPartCatalog


def get_car_series_service(
    session: AsyncSession = Depends(DBService.get_session),
) -> CarPartCatalog:
    return CarPartCatalogService(session=session, model=CarPartCatalog)
