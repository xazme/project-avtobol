from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .car_part_service import CarPartService
from .car_part_model import CarPart


def get_car_part_service(session: AsyncSession = Depends(DBService.get_session)):
    return CarPartService(session=session)
