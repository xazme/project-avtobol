# import asyncio
# from sqlalchemy import select, Result
# from sqlalchemy.orm import joinedload, selectinload
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.database import Base, DBService
# from app.car_parts.car_brand import CarBrand
# from app.car_parts.car_series import CarSeries

# from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

# engine = DBService.get_db_engine()

# async_session = async_sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     autoflush=False,
#     autocommit=False,
#     expire_on_commit=False,
# )


# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


# # async def create_order(session: AsyncSession, promo: str | None):
# #     new_order = Order(promo=promo)
# #     session.add(new_order)
# #     await session.commit()
# #     return new_order


# async def create_brand(session: AsyncSession, title: str):
#     brand = CarBrand(title=title)
#     session.add(brand)
#     await session.commit()
#     return brand


# async def create_series(
#     session: AsyncSession,
#     title: str,
#     year: str,
#     brand_id: int,
# ):
#     series = CarSeries(title=title, year=year, brand_id=brand_id)
#     session.add(series)
#     await session.commit()
#     return series


# async def main():
#     await create_tables()
#     async with async_session() as session:
#         brand1 = await create_brand(session=session, title="BMW")
#         series = await create_series(
#             session=session, title="RS7", year="2019-2099", brand_id=brand1.id
#         )

#     # print(brand1.title)

#     # for elem in brand1.series:
#     #     print(elem)


# asyncio.run(main())
