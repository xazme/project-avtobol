from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .disc_brand_model import DiscBrand
from .disc_brand_repository import DiscBrandRepository
from .disc_brand_handler import DiscBrandHandler


def get_disc_brand_handler(
    session: AsyncSession = Depends(DBService.get_session),
) -> DiscBrandHandler:
    repository = DiscBrandRepository(
        session=session,
        model=DiscBrand,
    )
    return DiscBrandHandler(
        repository=repository,
    )
