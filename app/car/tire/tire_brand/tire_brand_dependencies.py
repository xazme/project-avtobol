from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .tire_brand_model import TireBrand
from .tire_brand_repository import TireBrandRepository
from .tire_brand_handler import TireBrandHandler


def get_tire_brand_handler(
    session: AsyncSession = Depends(DBService.get_session),
) -> TireBrandRepository:
    repository = TireBrandHandler(
        session=session,
        model=TireBrand,
    )
    return TireBrandRepository(
        repository=repository,
    )
