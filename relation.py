import asyncio
from uuid import UUID
from app.database import Base
from sqlalchemy import Select, Result, Delete, and_, exists
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import func
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from app.database import DBService, Base
from app.user import User
from app.cart import Cart
from app.car import CarBrand, CarPartCatalog, CarSeries, Product

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
        # await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)
        pass


async def filter_products(
    session: AsyncSession,
    car_brand: UUID | None = None,
    car_series: UUID | None = None,
    car_part: UUID | None = None,
):
    stmt = Select(Product).filter_by(
        car_brand=car_brand,
        car_series=car_series,
        car_part=car_part,
    )

    result: Result = await session.execute(stmt)
    return result.scalars().all()


async def main():
    await create_tables()
    async with async_session() as session:
        filtered_product = await filter_products(
            session=session, car_brand="06316566-3114-4a11-8198-a5c6c9cd1fb9"
        )
        for product in filtered_product:
            print(product)


asyncio.run(main=main())
# Заполнение корзин пользователей
