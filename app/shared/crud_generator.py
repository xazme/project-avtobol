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

    async def get(self, id: str) -> T | None:
        stmt = Select(self.model).where(self.model.id == id).limit(1)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> T | None:
        print(data)
        obj = self.model(**data)

        try:
            self.session.add(obj)
            await self.session.commit()
            await self.session.refresh(obj)
            return obj

        except IntegrityError:
            await self.session.rollback()
            return None

    async def update(self, id: str, new_data: dict) -> T | None:
        obj = await self.get(id=id)

        if obj is None:
            return None

        for key, value in new_data.items():
            setattr(obj, key, value)

        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, id: str) -> bool | None:
        obj = await self.get(id=id)

        if obj is None:
            return None

        await self.session.delete(obj)
        await self.session.commit()
        return True

    async def get_by_name(self, name: str) -> T | None:
        stmt = Select(self.model).where(self.model.obj_name == name).limit(1)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()
