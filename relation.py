import asyncio
from typing import List
from sqlalchemy import String, Integer, ForeignKey, Select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService, Base

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


####################33
class CarPartCatalog(Base):
    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    car_part: Mapped[List["CarBrandPartSeriesAssoc"]] = relationship(
        back_populates="car_part",
    )


class CarBrand(Base):
    name: Mapped[str] = mapped_column(
        String,
        unique=True,
    )
    picture: Mapped[str] = mapped_column(
        String,
    )

    # relationship
    series: Mapped[List["CarSeries"]] = relationship(
        back_populates="brand",
    )
    car_part: Mapped[List["CarBrandPartSeriesAssoc"]] = relationship(
        back_populates="brand",
    )


class CarBrandPartSeriesAssoc(Base):
    brand_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("carbrand.id"),
        nullable=False,
    )
    car_part_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("carpartcatalog.id"),
        nullable=False,
    )
    series_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("carseries.id"),
        nullable=False,
    )

    # relationships
    brand: Mapped["CarBrand"] = relationship(back_populates="car_part")
    car_part: Mapped["CarPartCatalog"] = relationship(back_populates="car_part")
    series: Mapped["CarSeries"] = relationship(back_populates="car_part")


class CarSeries(Base):
    name: Mapped[str] = mapped_column(
        String,
        unique=True,
    )
    year: Mapped[str] = mapped_column(
        String,
        unique=False,
    )

    brand_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("carbrand.id"),
        index=True,
        unique=False,
    )

    # relationship
    brand: Mapped["CarBrand"] = relationship(
        back_populates="series",
    )

    car_part: Mapped[list["CarBrandPartSeriesAssoc"]] = relationship(
        back_populates="series",
    )


######################


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


async def get_carbrand(session: AsyncSession, id: int):
    stmt = Select(CarBrand).where(CarBrand.id == id)
    result: Result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_brand(session: AsyncSession, name: str, picture: str = "est"):
    brand = CarBrand(name=name, picture=picture)
    session.add(brand)
    await session.commit()
    return brand


async def create_series_v1(session: AsyncSession, brand_id: int, name: str, year: str):
    brand: CarBrand = await get_carbrand(session=session, id=brand_id)
    brand = await session.scalar(
        Select(CarBrand)
        .where(CarBrand.id == brand.id)
        .options(selectinload(CarBrand.series))
    )
    series = CarSeries(name=name, year=year)
    brand.series.append(series)
    await session.commit()
    return series


async def create_series_v2(session: AsyncSession, brand_id: int, name: str, year: str):
    brand: CarBrand = await get_carbrand(session=session, id=brand_id)
    series = CarSeries(name=name, year=year)
    brand.series = series
    await session.commit()
    return series


async def create_series_v3(session: AsyncSession, brand_id: int, name: str, year: str):
    series = CarSeries(brand_id=brand_id, name=name, year=year)
    session.add(series)
    await session.commit()
    return series


async def create_car_part(session: AsyncSession, name: str):
    car_part = CarPartCatalog(name=name)
    session.add(car_part)
    await session.commit()
    return car_part


async def create_car_part_full(
    session: AsyncSession, brand_id: int, car_part_id: int, series_id: int
):
    full_part = CarBrandPartSeriesAssoc(
        brand_id=brand_id, car_part_id=car_part_id, series_id=series_id
    )
    session.add(full_part)
    await session.commit()
    return full_part


async def get_all_series_by_brand_id(session: AsyncSession, brand_id: int):
    stmt = (
        Select(CarBrand)
        .where(CarBrand.id == brand_id)
        .options(selectinload(CarBrand.series))
    )
    res: Result = await session.execute(stmt)
    brand = res.scalar_one_or_none()
    return brand.series


async def get_all_part_by_brand_id(session: AsyncSession, brand_id: int):
    stmt = (
        Select(CarBrandPartSeriesAssoc)
        .where(CarBrandPartSeriesAssoc.brand_id == brand_id)
        .options(
            selectinload(CarBrandPartSeriesAssoc.brand),
            selectinload(CarBrandPartSeriesAssoc.car_part),
            selectinload(CarBrandPartSeriesAssoc.series),
        )
    )
    res: Result = await session.execute(stmt)
    parts = res.scalars().all()
    return parts


async def main():
    await create_tables()
    async with async_session() as session:
        # Создание брендов
        brand_mercedes = await create_brand(session=session, name="Mercedes")
        brand_audi = await create_brand(session=session, name="Audi")

        # Создание серий для каждого бренда
        series_merc_1 = await create_series_v3(
            session=session,
            brand_id=brand_mercedes.id,
            name="C-Class",
            year="2023",
        )
        series_merc_2 = await create_series_v3(
            session=session,
            brand_id=brand_mercedes.id,
            name="E-Class",
            year="2022",
        )

        series_audi_1 = await create_series_v3(
            session=session,
            brand_id=brand_audi.id,
            name="A4",
            year="2023",
        )
        series_audi_2 = await create_series_v3(
            session=session,
            brand_id=brand_audi.id,
            name="Q7",
            year="2022",
        )

        # Создание запчастей
        car_part_merc_1 = await create_car_part(session=session, name="Турбина")
        car_part_merc_2 = await create_car_part(session=session, name="Рулевая рейка")

        car_part_audi_1 = await create_car_part(session=session, name="Фары")
        car_part_audi_2 = await create_car_part(session=session, name="Тормозные диски")

        # Связывание запчастей с сериями
        await create_car_part_full(
            session=session,
            brand_id=brand_mercedes.id,
            car_part_id=car_part_merc_1.id,
            series_id=series_merc_2.id,
        )
        await create_car_part_full(
            session=session,
            brand_id=brand_mercedes.id,
            car_part_id=car_part_merc_2.id,
            series_id=series_merc_1.id,
        )

        await create_car_part_full(
            session=session,
            brand_id=brand_audi.id,
            car_part_id=car_part_audi_1.id,
            series_id=series_audi_1.id,
        )
        await create_car_part_full(
            session=session,
            brand_id=brand_audi.id,
            car_part_id=car_part_audi_2.id,
            series_id=series_audi_2.id,
        )

        brand_bmw = await create_brand(session=session, name="bmw")
        series_1 = await create_series_v3(
            session=session,
            brand_id=brand_bmw.id,
            name="E39",
            year="OLD",
        )
        series_2 = await create_series_v3(
            session=session,
            brand_id=brand_bmw.id,
            name="E79",
            year="OLD",
        )
        series_3 = await create_series_v3(
            session=session,
            brand_id=brand_bmw.id,
            name="E99",
            year="OLD",
        )

        car_part_1 = await create_car_part(session=session, name="BOMBA")
        car_part_2 = await create_car_part(session=session, name="DILDO")
        car_part_3 = await create_car_part(session=session, name="DVIGATEL")

        await create_car_part_full(
            session=session,
            brand_id=brand_bmw.id,
            car_part_id=car_part_1.id,
            series_id=series_3.id,
        )
        await create_car_part_full(
            session=session,
            brand_id=brand_bmw.id,
            car_part_id=car_part_2.id,
            series_id=series_2.id,
        )
        await create_car_part_full(
            session=session,
            brand_id=brand_bmw.id,
            car_part_id=car_part_3.id,
            series_id=series_1.id,
        )

        serieses = await get_all_series_by_brand_id(
            session=session, brand_id=brand_mercedes.id
        )
        # for i in serieses:
        #     print(i.name, i.id)
        parts = await get_all_part_by_brand_id(session=session, brand_id=brand_bmw.id)

        for part in parts:
            print(
                part.brand.name,
                part.brand.id,
                part.series.name,
                part.series.id,
                part.car_part.name,
                part.car_part.id,
            )


asyncio.run(main())
