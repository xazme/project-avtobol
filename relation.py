import asyncio
from app.database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService, Base

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

async_session = async_sessionmaker(
    bind=DBService.get_db_engine(),
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def create_tables():
    engine = DBService.get_db_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await create_tables()
    async with async_session() as session:
        pass


asyncio.run(main())
