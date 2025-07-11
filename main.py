import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

# client
from app.auth.auth_router import router as auth_router
from app.token.token_router import router as token_router
from app.user.user_router import router as user_router
from app.cart.cart_items.cart_item_router import router as cart_router

# product
from app.car.car_brand.car_brand_router import router as car_brand_router
from app.car.car_series.car_series_router import router as car_series_router
from app.car.car_part.car_part_router import router as car_part_router
from app.car.tire.tire_brand.tire_brand_router import router as tire_brand_router
from app.car.disc.disc_brand.disc_brand_router import router as disc_brand_router
from app.car.product.product_router import router as product_router

# storage
from app.storage.storage_router import router as s3_router

from app.core.config import settings
from app.database.db_service import DBService


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    await DBService.create_tables()
    # await broker.connect()

    yield

    await DBService.dispose()
    # await broker.close()
    # await DBService.drop_tables()


fastapi_app = FastAPI(lifespan=lifespan)


# faststream_app = FastStream(broker=broker)

# client routers
fastapi_app.include_router(auth_router)
fastapi_app.include_router(token_router)
fastapi_app.include_router(user_router)
fastapi_app.include_router(cart_router)

# product routers
fastapi_app.include_router(car_brand_router)
fastapi_app.include_router(car_series_router)
fastapi_app.include_router(car_part_router)
fastapi_app.include_router(tire_brand_router)
fastapi_app.include_router(disc_brand_router)
fastapi_app.include_router(product_router)

# storage router
fastapi_app.include_router(s3_router)


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
