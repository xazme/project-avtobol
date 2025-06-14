from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .tires_model import Tires
from .tires_repository import TiresRepository
from .tires_handler import TiresHandler


def get_tires_handler(
    session: AsyncSession = Depends(DBService.get_session),
) -> TiresHandler:
    repository = TiresRepository(
        session=session,
        model=Tires,
    )
    return TiresHandler(repository=repository)
