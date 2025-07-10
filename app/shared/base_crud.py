from uuid import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Select, Result, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class BaseCRUD:
    """CRUD GENERATOR"""

    def __init__(self, session: AsyncSession, model: DeclarativeBase):
        self.session: AsyncSession = session
        self.model: DeclarativeBase = model

    async def create(
        self,
        data: dict,
    ) -> DeclarativeBase | None:
        obj: DeclarativeBase = self.model(**data)
        try:
            self.session.add(obj)
            await self.session.commit()
            await self.session.refresh(obj)
            return obj
        except IntegrityError as e:
            print(e)
            await self.session.rollback()
            return None

    async def update_by_id(
        self,
        id: UUID,
        data: dict,
    ) -> DeclarativeBase | None:
        obj: DeclarativeBase | None = await self.get_by_id(id=id)
        if obj is None:
            return None
        try:
            for key, value in data.items():
                setattr(obj, key, value)

            await self.session.commit()
            await self.session.refresh(obj)
            return obj
        except IntegrityError as e:
            await self.session.rollback()
            return None

    async def delete_by_id(
        self,
        id: UUID,
    ) -> bool | None:
        obj: DeclarativeBase | None = await self.get_by_id(id=id)

        if obj is None:
            return None

        await self.session.delete(obj)
        await self.session.commit()
        return True

    async def get_by_id(
        self,
        id: UUID,
    ) -> DeclarativeBase | None:
        stmt: Select = Select(self.model).where(self.model.id == id).limit(1)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_by_name(
        self,
        name: str,
    ) -> DeclarativeBase | None:
        stmt: Select = Select(self.model).where(self.model.name == name)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self,
    ) -> list[DeclarativeBase]:
        stmt: Select = Select(self.model).order_by(self.model.id)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_all_pagination(
        self,
        query: str,
        page: int,
        page_size: int,
    ) -> list[DeclarativeBase]:
        stmt: Select = (
            Select(self.model)
            .where(self.model.name.like(f"{query}%"))
            .limit(limit=page_size)
            .offset((page - 1) * page_size)
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_all_by_scroll(
        self,
        query: str,
        cursor: int | None,
        take: int | None,
    ) -> tuple[int | None, list]:
        cursor = cursor if cursor is not None else 0
        stmt_count: Select = Select(func.count(self.model.id))
        stmt: Select = (
            Select(self.model).offset(cursor).where(self.model.name.like(f"{query}%"))
        )
        if take is not None:
            stmt = stmt.limit(take)

        result: Result = await self.session.execute(statement=stmt)
        result_count: Result = await self.session.execute(statement=stmt_count)
        count = result_count.scalar()

        next_cursor = (
            cursor + take if take is not None and (cursor + take) <= count else None
        )

        return next_cursor, result.scalars().all()
