from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db_service import DBService
from app.shared import CRUDGenerator
from .user_model import User


async def get_user_service(
    session: AsyncSession = Depends(DBService.get_session),
) -> CRUDGenerator:
    return CRUDGenerator[User](session=session, model=User)
