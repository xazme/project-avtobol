from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .disc_model import Disc
from .disc_repository import DiscRepository
from .disc_handler import DiscHandler


def get_disc_handler(
    session: AsyncSession = Depends(DBService.get_session),
) -> DiscHandler:
    repository = DiscRepository(
        session=session,
        model=Disc,
    )
    return DiscRepository(repository=repository)
