from typing import TypeVar, Generic, Type
from sqlalchemy import Select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class CRUDGenerator(Generic[T]):
    """CRUD GENERATOR"""

    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def get(self, obj_id: int) -> T | None:
        stmt = Select(self.model).where(self.model.id == obj_id).limit(1)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> T | None:
        obj = self.model(**data)
        try:
            self.session.add(obj)
            await self.session.commit()
            await self.session.refresh(obj)
            return obj

        except IntegrityError:
            await self.session.rollback()
            return None

    async def update(self, obj_id: int, new_data: dict) -> T | None:
        obj = await self.get(obj_id=obj_id)

        if obj is None:
            return None

        for key, value in new_data.items():
            setattr(obj, key, value)

        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: int) -> bool | None:
        obj = await self.get(obj_id=obj_id)

        if obj is None:
            return None

        await self.session.delete(obj)
        await self.session.commit()
        return True

    async def get_by_name(self, obj_name: str) -> T | None:
        stmt = Select(self.model).where(self.model.obj_name == obj_name).limit(1)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list:
        stmt = Select(self.model.obj_name, self.model.id)
        result: Result = await self.session.execute(statement=stmt)
        rows = result.all()
        return [(row) for row in rows]
