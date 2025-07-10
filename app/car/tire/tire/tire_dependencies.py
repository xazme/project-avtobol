from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .tire_model import Tire
from .tire_repository import TireRepository
from .tire_handler import TireHandler


def get_tire_handler(
    session: AsyncSession = Depends(DBService.get_session),
) -> TireHandler:
    repository = TireRepository(
        session=session,
        model=Tire,
    )
    return TireHandler(repository=repository)
