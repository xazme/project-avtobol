# import asyncio
# from faststream import FastStream, Depends
# from faststream.rabbit import RabbitBroker
# from app.database import DBService
# from app.car.car_brand.car_brand_dependencies import get_car_brand_handler
# from app.car.car_brand.car_brand_schema import CarBrandCreate

# broker = RabbitBroker(
#     url="amqp://admin:adminpass@localhost:5672",
#     apply_types=True,
# )
# app = FastStream(broker=broker)

# import pydantic


# class Schema(pydantic.BaseModel):
#     text: str = pydantic.Field(...)
#     grams: int = pydantic.Field(...)


# @broker.subscriber(queue="input")
# async def process(msg: Schema, session=Depends(DBService.get_session)):
#     pass


# @app.on_startup
# async def startup():
#     await broker.connect()


# @app.after_startup
# async def do_smth():
#     msg = Schema(
#         text="разработчик вместо того чтобы делать доку норм нюхал кокос",
#         grams=120,
#     )
#     await broker.publish(
#         message=msg,
#         queue="input",
#         content_type="application/json",
#     )


# if __name__ == "__main__":
#     asyncio.run(app.run())
