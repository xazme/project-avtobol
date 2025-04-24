import asyncio
from sqlalchemy import Select, Result, Integer, String, func
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


def gen_smth():
    return int(uuid.uuid4()) >> 96


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models"""

    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        nullable=False,
        primary_key=True,
        index=True,
        default=gen_smth,
    )


class CarBrand(Base):
    __tablename__ = "pi"
    name: Mapped[str] = mapped_column(
        String,
        unique=True,
    )
    url: Mapped[str] = mapped_column(
        String,
        unique=True,
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


# async def create_series(
#     session: AsyncSession,
#     name: str,
#     year: str,
#     brand_id: any,
# ):
#     series = CarSeries(name=name, year=year, brand_id=brand_id)
#     session.add(series)
#     await session.commit()
#     return series


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
    stmt = Select(CarBrand).order_by(CarBrand.id)
    res: Result = await session.execute(statement=stmt)
    return res.scalars().all()


async def main():
    await create_tables()
    async with async_session() as session:
        brand2 = await create_brand(session=session, title="zxc", url="123123")

        # serie = await create_series(
        #     session=session, name="adasda", year="1123", brand_id=brand2.id
        # )

        # serie2 = await create_series(
        #     session=session, name="qeqeuy", year="qrqwr", brand_id=brand2.id
        # )

        # bomba = await get_smth(session=session, brand=brand2)

        # for z in bomba:
        #     print(z)
        #     for kk in z.series:
        #         print(kk.name)


asyncio.run(main())
