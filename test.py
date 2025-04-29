import asyncio
from sqlalchemy import Select, Result, Integer, String, func
from pydantic import BaseModel
import uuid
from sqlalchemy.orm import (
    joinedload,
    selectinload,
    DeclarativeBase,
    Mapped,
    mapped_column,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Base, DBService
from app.car_parts.car_brand_series_assoc import CarBrandPartSeriesAssoc
from app.car_parts import CarBrand, CarPartCatalog, CarSeries

# from app.car_parts.car_brand import CarBrand

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

engine = DBService.get_db_engine()

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


class Bbbeb(BaseModel):
    brand: str
    part: str
    series: str


def gen_smth():
    return int(uuid.uuid4()) >> 96


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


async def create_series(session: AsyncSession, title: str, year: str, brand_id: int):
    brand = CarSeries(name=title, year=year, brand_id=brand_id)
    session.add(brand)
    await session.commit()
    return brand


async def create_part(session: AsyncSession, name: str):
    ads = CarPartCatalog(name=name)
    session.add(ads)
    await session.commit()
    return ads


async def create_car_part(session: AsyncSession, brand_id, series_id, car_part_id):
    asdasd = CarBrandPartSeriesAssoc(
        brand_id=brand_id, car_part_id=car_part_id, series_id=series_id
    )
    session.add(asdasd)
    await session.commit()
    return asdasd


async def get_smth(session: AsyncSession, brand: any):
    stmt = (
        Select(CarBrand)
        .options(selectinload(CarBrand.series))
        .where(CarBrand.id == brand.id)
    )
    res: Result = await session.execute(statement=stmt)
    be = res.scalars()
    return list(be)


async def get_all_parts(session: AsyncSession):
    stmt = Select(CarBrandPartSeriesAssoc).options(
        selectinload(
            CarBrandPartSeriesAssoc.car_part,
        ),
        selectinload(
            CarBrandPartSeriesAssoc.brand,
        ),
        selectinload(
            CarBrandPartSeriesAssoc.series,
        ),
    )
    result: Result = await session.execute(statement=stmt)
    list = result.scalars().all()
    return list


async def get_part_by_id(session: AsyncSession, id_of_shit):
    stmt = (
        Select(CarBrandPartSeriesAssoc)
        .where(CarBrandPartSeriesAssoc.id == id_of_shit)
        .options(
            selectinload(CarBrandPartSeriesAssoc.brand),
            selectinload(CarBrandPartSeriesAssoc.series),
            selectinload(CarBrandPartSeriesAssoc.car_part),
        )
    )
    res: Result = await session.execute(stmt)
    return res.scalar_one_or_none()


async def create_blabla(session: AsyncSession, brand_id, series_id, part_id: int):
    bebe = CarBrandPartSeriesAssoc(
        brand_id=brand_id, car_part_id=part_id, series_id=series_id
    )
    session.add(bebe)
    await session.commit()


async def get_all(session: AsyncSession):
    stmt = Select(CarBrand).order_by(CarBrand.id)
    res: Result = await session.execute(statement=stmt)
    return res.scalars().all()


def convert_data_for_car_brand_series_object(list_of_car_parts: list):
    data = []
    for car_part in list_of_car_parts:
        bebe = {
            "brand name": car_part.brand.name,
            "series name": car_part.series.name,
            "part type": car_part.car_part.name,
        }
        data.append(bebe)
    print(data)


async def main():
    await create_tables()
    async with async_session() as session:
        # Создаём бренд
        brand1 = await create_brand(session=session, title="ASDAWEQ", url="VZXCZ")
        # Создаём 3 серии, принадлежащие этому бренду
        series1 = await create_series(
            session=session, title="adsasd", year="1991", brand_id=brand1.id
        )
        series2 = await create_series(
            session=session, title="qwerqfa", year="1991", brand_id=brand1.id
        )
        series3 = await create_series(
            session=session, title="adwqf", year="1991", brand_id=brand1.id
        )

        # Создаём 3 запчасти
        part1 = await create_part(session=session, name="дрочила")
        part2 = await create_part(session=session, name="зубрила")
        part3 = await create_part(session=session, name="PIMDODO")

        await create_blabla(
            session=session,
            brand_id=brand1.id,
            series_id=series1.id,
            part_id=part1.id,
        )

        all = await get_all_parts(session=session)
        convert_data_for_car_brand_series_object(list_of_car_parts=all)


asyncio.run(main())
