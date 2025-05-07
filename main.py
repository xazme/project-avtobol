from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from app.user import user_router
from app.auth import auth_router
from app.car.car_brand import car_brand_router
from app.car.car_series import car_series_router
from app.car.car_brand_series_assoc import car_part_router
from app.car.car_part_catalog import car_part_catalog_router
from app.core.config import settings
from app.database.db_service import DBService
from app.storage.storage_service_dependencies import storage_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DBService.create_tables()
    await storage_service.create_bucket()
    yield
    await DBService.drop_tables()  # TODO turn off
    await storage_service.delete_bucket()
    await DBService.dispose()


app = FastAPI(
    lifespan=lifespan,
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(car_brand_router)
app.include_router(car_series_router)
app.include_router(car_part_router)
app.include_router(car_part_catalog_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )

# Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
