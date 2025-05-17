from app.shared import BaseCRUD
from sqlalchemy import Select, Result
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession


class TokenRepository(BaseCRUD):

    def __init__(
        self,
        session: AsyncSession,
        model: DeclarativeBase,
    ):
        super().__init__(session, model)

    async def get_token_by_owner(
        self,
        id: int,
    ) -> DeclarativeBase | None:
        stmt = Select(self.model).where(self.model.user_id == id)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def update_access_token(
        self,
        user_id: int,
        data: dict,
    ) -> DeclarativeBase | None:
        token = await self.get_token_by_owner(id=user_id)

        if token is None:
            return None

        for key, value in data.items():
            setattr(token, key, value)

        await self.session.commit()
        await self.session.refresh(token)
        return token

    async def delete_token(self, user_id):
        token = await self.get_token_by_owner(id=user_id)

        if token is None:
            return None

        await self.session.delete(token)
        await self.session.commit()
        return True

    async def get_access_token(
        self,
        token: str,
    ) -> DeclarativeBase | None:
        stmt = Select(self.model).where(self.model.access_token == token)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_refresh_token(
        self,
        token: str,
    ) -> DeclarativeBase | None:
        stmt = Select(self.model).where(self.model.refresh_token == token)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()
