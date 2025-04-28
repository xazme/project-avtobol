from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDGenerator:
    """CRUD GENERATOR"""

    def __init__(self, session: AsyncSession, model: DeclarativeBase):
        self.session = session
        self.model = model

    async def get(self, id: int) -> DeclarativeBase | None:
        stmt = Select(self.model).where(self.model.id == id).limit(1)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> DeclarativeBase | None:
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

    async def update(self, id: int, new_data: dict) -> DeclarativeBase | None:
        obj = await self.get(id=id)

        if obj is None:
            return None

        for key, value in new_data.items():
            setattr(obj, key, value)

        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, id: int) -> bool | None:
        obj = await self.get(id=id)

        if obj is None:
            return None

        await self.session.delete(obj)
        await self.session.commit()
        return True

    async def get_by_name(self, name: str) -> DeclarativeBase | None:
        stmt = Select(self.model).where(self.model.name == name).limit(1)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list:
        stmt = Select(self.model).order_by(self.model.id)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()
