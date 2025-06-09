from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .car_part_catalog_repository import CarPartRepository
from .car_part_catalog_handler import CarPartHandler
from .car_part_catalog_model import CarPart


def get_car_part_handler(
    session: AsyncSession = Depends(DBService.get_session),
) -> CarPartHandler:
    car_part_repository = CarPartRepository(
        session=session,
        model=CarPart,
    )
    return CarPartHandler(repository=car_part_repository)
