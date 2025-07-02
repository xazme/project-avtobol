from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from .token_model import Token


class TokenRepository(BaseCRUD):

    def __init__(self, session: AsyncSession, model: Token):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: Token = model

    async def delete_refresh_token_by_user_id(
        self,
        user_id: UUID,
    ) -> bool:
        token: Token | None = await self.get_user_tokens_by_id(user_id=user_id)
        try:
            await self.session.delete(token)
            await self.session.commit()
            return True
        except SQLAlchemyError as e:
            return False

    async def get_refresh_token_by_token(
        self,
        token: str,
    ) -> Token | None:
        stmt: Select = Select(self.model).where(self.model.refresh_token == token)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_user_tokens_by_id(
        self,
        user_id: UUID,
    ) -> Token | None:
        stmt: Select = Select(self.model).where(self.model.user_id == user_id)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()
