from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db_service import DBService
from .user_handler import UserHandler
from .user_model import User
from .user_repository import UserRepository


async def get_user_handler(
    session: AsyncSession = Depends(DBService.get_session),
) -> UserHandler:
    repository = UserRepository(
        session=session,
        model=User,
    )
    return UserHandler(repository=repository)
