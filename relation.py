import asyncio
from app.database import Base
from sqlalchemy import Select, Result, Delete
from sqlalchemy.orm import selectinload
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
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_user(session: AsyncSession, email, password):
    user = User(email=email, password=password)
    session.add(user)
    await session.commit()
    return user


async def create_cart(session: AsyncSession, user_id, product_id):
    elem = Cart(
        user_id=user_id,
        product_id=product_id,
    )
    session.add(elem)
    await session.commit()


async def create_brand(session: AsyncSession, name: str) -> CarBrand:
    brand = CarBrand(name=name)
    session.add(brand)
    await session.commit()
    await session.refresh(brand)
    return brand


async def create_series_v3(
    session: AsyncSession, brand_id: int, name: str, year: str
) -> CarSeries:
    series = CarSeries(brand_id=brand_id, name=name, year=year)
    session.add(series)
    await session.commit()
    await session.refresh(series)
    return series


async def create_car_part(session: AsyncSession, name: str) -> CarPartCatalog:
    car_part = CarPartCatalog(name=name)
    session.add(car_part)
    await session.commit()
    await session.refresh(car_part)
    return car_part


async def create_car_part_full(
    session: AsyncSession, brand_id: int, car_part_id: int, series_id: int
) -> Product:
    assoc = Product(
        brand_id=brand_id,
        car_part_id=car_part_id,
        series_id=series_id,
    )
    session.add(assoc)
    await session.commit()
    await session.refresh(assoc)
    return assoc


async def get_user_cart(session: AsyncSession, id):
    stmt = Select(Cart).where(Cart.user_id == id)
    result: Result = await session.execute(stmt)
    positions = result.scalars().all()
    return positions


async def delete_all_positions(session: AsyncSession, user_id: int):
    count: Result = await session.execute(
        Select(func.count()).select_from(Cart).where(Cart.user_id == user_id)
    )
    if count.scalar() <= 0:
        return None

    stmt = Delete(Cart).where(Cart.user_id == user_id)
    result: Result = await session.execute(statement=stmt)
    await session.commit()
    return result


async def main():
    await create_tables()
    async with async_session() as session:
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
        product_1 = await create_car_part_full(
            session=session,
            brand_id=brand_mercedes.id,
            car_part_id=car_part_merc_2.id,
            series_id=series_merc_1.id,
        )

        product_2 = await create_car_part_full(
            session=session,
            brand_id=brand_audi.id,
            car_part_id=car_part_audi_1.id,
            series_id=series_audi_1.id,
        )
        product_3 = await create_car_part_full(
            session=session,
            brand_id=brand_audi.id,
            car_part_id=car_part_audi_2.id,
            series_id=series_audi_2.id,
        )

        # Генерация пользователей
        user_1 = await create_user(
            session=session, email="user1@example.com", password="securepass1"
        )
        user_2 = await create_user(
            session=session, email="user2@example.com", password="securepass2"
        )
        user_3 = await create_user(
            session=session, email="user3@example.com", password="securepass3"
        )

        # Создание товаров
        product_4 = await create_car_part_full(
            session=session,
            brand_id=brand_mercedes.id,
            car_part_id=car_part_merc_1.id,
            series_id=series_merc_2.id,
        )
        product_5 = await create_car_part_full(
            session=session,
            brand_id=brand_mercedes.id,
            car_part_id=car_part_merc_2.id,
            series_id=series_merc_1.id,
        )
        product_6 = await create_car_part_full(
            session=session,
            brand_id=brand_audi.id,
            car_part_id=car_part_audi_1.id,
            series_id=series_audi_1.id,
        )
        product_7 = await create_car_part_full(
            session=session,
            brand_id=brand_audi.id,
            car_part_id=car_part_audi_2.id,
            series_id=series_audi_2.id,
        )

        # Заполнение корзин пользователей
        await create_cart(session=session, user_id=user_1.id, product_id=product_1.id)
        await create_cart(session=session, user_id=user_1.id, product_id=product_4.id)

        await create_cart(session=session, user_id=user_2.id, product_id=product_2.id)
        await create_cart(session=session, user_id=user_2.id, product_id=product_5.id)

        await create_cart(session=session, user_id=user_3.id, product_id=product_3.id)
        await create_cart(session=session, user_id=user_3.id, product_id=product_6.id)
        await create_cart(session=session, user_id=user_3.id, product_id=product_7.id)

        # all = await get_user_cart(
        #     session=session,
        #     id=user_1.id,
        # )
        print(user_2.id)
        print("SSSSSSSSSSSSS")
        res = await delete_all_positions(
            session=session,
            user_id=user_1.id,
        )
        # print(res)
        # res = await delete_all_positions(
        #     session=session,
        #     user_id=user_2.id,
        # )
        # print(res)
        # res = await delete_all_positions(
        #     session=session,
        #     user_id=user_3.id,
        # )
        # print(res)
        # res = await delete_all_positions(
        #     session=session,
        #     user_id=user_1.id,
        # )
        print(res)


asyncio.run(main())
