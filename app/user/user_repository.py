from sqlalchemy import Select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from .user_model import User


class UserRepository(BaseCRUD):

    def __init__(
        self,
        session: AsyncSession,
        model: User,
    ):
        super().__init__(session, model)

    async def get_user_by_email(
        self,
        email: str,
    ):
        stmt = Select(self.model).where(self.model.email == email)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()
