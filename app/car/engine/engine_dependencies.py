from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .engine_model import Engine
from .engine_repository import EngineRepository
from .engine_handler import EngineHandler


def get_engine_handler(
    session: AsyncSession = Depends(DBService.get_session),
) -> EngineHandler:
    repository = EngineRepository(
        session=session,
        model=Engine,
    )
    return EngineHandler(repository=repository)
