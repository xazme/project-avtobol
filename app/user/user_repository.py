from uuid import UUID
from sqlalchemy import Select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.shared import BaseCRUD
from .user_model import User
from .user_enums import UserRoles


class UserRepository(BaseCRUD):

    def __init__(self, session: AsyncSession, model: type[User]):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: type[User] = model

    async def change_user_role(
        self,
        id: UUID,
        new_role: UserRoles,
    ) -> User | None:
        user: User | None = await self.get_by_id(id=id)
        if not user:
            return None
        try:
            user.role = new_role
            await self.session.refresh(user)
            return user
        except IntegrityError:
            await self.session.rollback()
            return None

    async def get_user_by_phone_number(
        self,
        phone_number: str,
    ) -> User | None:
        stmt: Select = Select(self.model).where(self.model.phone_number == phone_number)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_user_by_id(
        self,
        id: UUID,
    ) -> User | None:
        return await self.get_by_id(id=id)

    async def get_user_by_name(
        self,
        name: str,
    ) -> User | None:
        return await self.get_by_name(name=name)
