from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db_service import DBService
from .user_service import UserService


async def get_user_service(
    session: AsyncSession = Depends(DBService.get_session),
) -> UserService:
    return UserService(session=session)
