from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from app.core.config import settings
from .base import Base


class DBService:

    engine: AsyncEngine = create_async_engine(
        url=settings.db.get_db_url(),
        echo=True,
        pool_size=10,
        max_overflow=20,
    )

    session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
    )

    @classmethod
    def get_db_engine(cls) -> AsyncEngine:
        return cls.engine

    @classmethod
    async def dispose(cls):
        await cls.get_db_engine().dispose()

    @classmethod
    async def get_session(cls) -> AsyncGenerator[AsyncSession, None]:
        """Session getter"""
        async with cls.session() as session:
            yield session

    @classmethod
    async def create_tables(cls) -> None:
        """Create Tables"""

        async with cls.engine.begin() as con:
            await con.run_sync(Base.metadata.create_all)

    @classmethod
    async def drop_tables(cls) -> None:
        """Delete Tables"""
        async with cls.engine.begin() as con:
            await con.run_sync(Base.metadata.drop_all)
