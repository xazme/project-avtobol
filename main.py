import uvicorn
import threading
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from faststream import FastStream
import uvicorn.server
from app.user import user_router
from app.auth import auth_router
from app.token import token_router
from app.car import car_router
from app.cart import cart_router
from app.order import order_router
from app.core.config import settings
from app.faststream import broker
from app.database.db_service import DBService


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    # await DBService.create_tables()
    await broker.connect()

    yield

    await DBService.dispose()
    # await DBService.drop_tables()
    # await broker.close()


fastapi_app = FastAPI(lifespan=lifespan)
faststream_app = FastStream(broker=broker)

# broker.include_router(router=product_router)
# broker.include_router(router=brand_router)
fastapi_app.include_router(auth_router)
fastapi_app.include_router(car_router)
fastapi_app.include_router(user_router)
fastapi_app.include_router(cart_router)
fastapi_app.include_router(order_router)
fastapi_app.include_router(token_router)


def run_fastapi():
    uvicorn.run(
        "main:fastapi_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )


def main():
    run_fastapi()


if __name__ == "__main__":
    main()

# Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
