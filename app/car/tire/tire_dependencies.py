from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .tire_model import Tire
from .tire_repository import TiresRepository
from .tire_handler import TiresHandler


def get_tires_handler(
    session: AsyncSession = Depends(DBService.get_session),
) -> TiresHandler:
    repository = TiresRepository(
        session=session,
        model=Tire,
    )
    return TiresHandler(repository=repository)
