from fastapi import APIRouter
from .car_brand import CarBrand, car_brand_router
from .car_part_catalog import CarPartCatalog, car_part_catalog_router
from .car_series import CarSeries, car_series_router
from .product import Product, product_router

routers = [
    car_part_catalog_router,
    car_brand_router,
    car_series_router,
    product_router,
]

car_router = APIRouter()

for router in routers:
    car_router.include_router(router)
