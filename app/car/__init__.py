from fastapi import APIRouter
from .car_brand import CarBrand, car_brand_router
from .car_part_catalog import CarPartCatalog, car_part_catalog_router
from .car_series import car_series_router
from .car_brand_series_assoc import CarBrandPartSeriesAssoc, car_brand_series_router

routers = [
    car_part_catalog_router,
    car_brand_router,
    car_brand_series_router,
    car_series_router,
]

car_router = APIRouter(prefix="/razborka")

for router in routers:
    car_router.include_router(router)
