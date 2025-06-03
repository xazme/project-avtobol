import asyncio
from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitRouter

broker = RabbitBroker(url="amqp://admin:adminpass@localhost:5672")
app = FastStream(broker=broker)
router = RabbitRouter()


@router.subscriber(queue="input")
@router.publisher(queue="output")
async def handle(msg: str):
    return msg


@router.subscriber(queue="output")
async def process(msg):
    print(msg)


@app.on_startup
async def startup():
    await broker.connect()


@app.after_startup
async def do_smth():
    await broker.publish(
        message="doob",
        queue="input",
        content_type="text/plain",
    )


broker.include_router(router=router)

if __name__ == "__main__":
    asyncio.run(app.run())
