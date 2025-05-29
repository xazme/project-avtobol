from uuid import UUID
from sqlalchemy import Select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from .token_model import Token


class TokenRepository(BaseCRUD):

    def __init__(
        self,
        session: AsyncSession,
        model: Token,
    ):
        super().__init__(session=session, model=model)
        self.session = session
        self.model = model

    async def update_user_access_token(
        self,
        user_id: UUID,
        data: dict,
    ) -> Token | None:
        token = await self.get_user_tokens_by_id(user_id=user_id)

        if token is None:
            return None

        for key, value in data.items():
            setattr(token, key, value)

        await self.session.commit()
        await self.session.refresh(token)
        return token

    async def delete_tokens_by_user_id(
        self,
        user_id: UUID,
    ) -> bool | None:
        token = await self.get_user_tokens_by_id(user_id=user_id)

        if token is None:
            return None

        await self.session.delete(token)
        await self.session.commit()
        return True

    async def get_access_token_by_token(
        self,
        token: str,
    ) -> Token | None:
        stmt = Select(self.model).where(self.model.access_token == token)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_refresh_token_by_token(
        self,
        token: str,
    ) -> Token | None:
        stmt = Select(self.model).where(self.model.refresh_token == token)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_user_tokens_by_id(
        self,
        user_id: UUID,
    ) -> Token | None:
        stmt = Select(self.model).where(self.model.user_id == user_id)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()
