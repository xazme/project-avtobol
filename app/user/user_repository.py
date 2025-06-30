from uuid import UUID
from sqlalchemy import Select, Result, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.shared import BaseCRUD
from .user_model import User
from .user_enums import UserRoles
from .user_schema import UserFilters


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

    async def get_all_users_by_scroll(
        self,
        user_filters: UserFilters,
        cursor: int | None,
        take: int | None,
    ) -> tuple[int | None, list]:
        filters = await self.prepare_user_filters(filters=user_filters)
        cursor = cursor if cursor is not None else 0
        stmt_count: Select = Select(func.count(self.model.id))
        stmt: Select = Select(self.model).offset(cursor).where(and_(*filters))
        if take is not None:
            stmt = stmt.limit(take)

        result: Result = await self.session.execute(statement=stmt)
        result_count: Result = await self.session.execute(statement=stmt_count)
        count = result_count.scalar()

        next_cursor = (
            cursor + take if take is not None and (cursor + take) <= count else None
        )

        return next_cursor, result.scalars().all()

    async def prepare_user_filters(self, filters: UserFilters) -> list:
        filters_list = []

        if filters.name:
            filters_list.append(self.model.name.ilike(f"%{filters.name}%"))

        if filters.phone_number:
            filters_list.append(
                self.model.phone_number.ilike(f"%{filters.phone_number}%")
            )

        if filters.status:
            filters_list.append(self.model.status == filters.status)

        if filters.role:
            filters_list.append(self.model.role == filters.role)

        if filters.created_from:
            filters_list.append(self.model.created_at >= filters.created_from)

        if filters.created_to:
            filters_list.append(self.model.created_at <= filters.created_to)

        return filters_list

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
