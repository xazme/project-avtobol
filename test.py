import asyncio
from sqlalchemy import Select, Result
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Base, DBService
from app.car_parts.car_brand import CarBrand
from app.car_parts.car_series import CarSeries

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

engine = DBService.get_db_engine()

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# async def create_order(session: AsyncSession, promo: str | None):
#     new_order = Order(promo=promo)
#     session.add(new_order)
#     await session.commit()
#     return new_order


async def create_brand(session: AsyncSession, title: str, url: str):
    brand = CarBrand(name=title, url=url)
    session.add(brand)
    await session.commit()
    return brand


async def create_series(
    session: AsyncSession,
    name: str,
    year: str,
    brand_id: any,
):
    series = CarSeries(name=name, year=year, brand_id=brand_id)
    session.add(series)
    await session.commit()
    return series


async def get_smth(session: AsyncSession, brand: any):
    stmt = (
        Select(CarBrand)
        .options(selectinload(CarBrand.series))
        .where(CarBrand.id == brand.id)
    )
    res: Result = await session.execute(statement=stmt)
    return res.scalars().all()


async def get_all(session: AsyncSession):
    stmt = Select(CarBrand).order_by(CarBrand.id)
    res: Result = await session.execute(statement=stmt)
    return res.scalars().all()


async def main():
    await create_tables()
    async with async_session() as session:
        brand2 = await create_brand(session=session, title="zxc", url="123123")

        print(brand2.id)
        print("777777777777777777777777777")

        serie = await create_series(
            session=session, name="adasda", year="1123", brand_id=brand2.id
        )

        bomba = await get_smth(session=session, brand=brand2)

        for elem in bomba:
            for sex in elem.series:
                print(sex.year)

    # for elem in brand1.series:
    #     print(elem)


asyncio.run(main())
