from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .car_brand_service import CarBrandService
from .car_brand_model import CarBrand


def get_car_brand_service(
    session: AsyncSession = Depends(DBService.get_session),
) -> CarBrandService:
    return CarBrandService(session=session, model=CarBrand)
