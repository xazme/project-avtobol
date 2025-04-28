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


async def create_dirt(session: AsyncSession, brand_id, series_id, car_part_id):
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


async def get_all(session: AsyncSession):
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


async def get_all(session: AsyncSession):
    stmt = Select(CarBrand).order_by(CarBrand.id)
    res: Result = await session.execute(statement=stmt)
    return res.scalars().all()


async def main():
    await create_tables()
    async with async_session() as session:
        brand2 = await create_brand(session=session, title="zxc", url="123123")
        series = await create_series(
            session=session, title="BOBMA", year="1990", brand_id=brand2.id
        )
        series = await create_series(
            session=session, title="adsasd", year="1991", brand_id=brand2.id
        )
        part = await create_part(session=session, name="seqweqx")
        part2 = await create_part(session=session, name="seasdx")
        part3 = await create_part(session=session, name="zxczxc")

        jopa = await create_dirt(
            session=session,
            brand_id=brand2.id,
            series_id=series.id,
            car_part_id=part.id,
        )

        bem = await get_smth(session=session, brand=brand2)

        suka_id = brand2.id

        negr = await session.scalar(
            Select(CarBrand)
            .where(CarBrand.id == suka_id)
            .options(selectinload(CarBrand.car_part))
        )

        id_of_part = negr.car_part.id
        print(id_of_part)

        # for kn in bem:
        #     for nm in kn.series:
        #         mem = {
        #             "brand name": kn.name,
        #             "brand id": kn.id,
        #             "part id": kn.car_part.car_part_id,
        #             "series": nm.name,
        #         }
        #         print(mem)

        bebe = await get_part_by_id(session=session, id_of_shit=id_of_part)
        print(bebe.brand.name)


asyncio.run(main())
