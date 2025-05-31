from typing import TYPE_CHECKING
from uuid import UUID
from fastapi import APIRouter, Depends, status, File, UploadFile
from app.core import settings
from app.car.car_series import get_car_series_handler
from .product_schema import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from .product_dependencies import get_product_handler
from .product_helper import convert_data_for_product
from .product_schema import ProductFilters

if TYPE_CHECKING:
    from app.car.car_series import CarSeriesHandler
    from .product_handler import ProductHandler

router = APIRouter(prefix=settings.api.product, tags=["Product"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponse,
)
async def get_product(
    product_id: UUID,
    product_handler: "ProductHandler" = Depends(get_product_handler),
):
    product = await product_handler.get_product_by_id(product_id=product_id)
    return ProductResponse.model_validate(product)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=list,
)
async def get_all_products(
    page: int,
    page_size: int,
    filters: ProductFilters = Depends(),
    product_handler: "ProductHandler" = Depends(get_product_handler),
):
    products = await product_handler.get_all_products(
        page=page,
        page_size=page_size,
        filters=filters,
    )
    return [ProductResponse.model_validate(product) for product in products]


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponse,
)
async def create_product(
    product_data: ProductCreate = Depends(),
    product_pictures: list[UploadFile] = File(...),
    series_handler: "CarSeriesHandler" = Depends(get_car_series_handler),
    product_handler: "ProductHandler" = Depends(get_product_handler),
):
    await series_handler.check_relation(
        car_brand_id=product_data.car_brand_id,
        car_series_id=product_data.car_series_id,
    )
    car_part = await product_handler.create_product(
        data=product_data,
        files=product_pictures,
    )
    return ProductResponse.model_validate(car_part)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponse,
)
async def update_product(
    product_id: UUID,
    new_product_data: ProductUpdate = Depends(),
    new_product_pictures: list[UploadFile] | None = File(...),
    series_handler: "CarSeriesHandler" = Depends(get_car_series_handler),
    product_handler: "ProductHandler" = Depends(get_product_handler),
):
    await series_handler.check_relation(
        car_brand_id=new_product_data.car_brand_id,
        car_series_id=new_product_data.car_series_id,
    )
    upd_product = await product_handler.update_product(
        id=product_id,
        data=new_product_data,
        files=new_product_pictures,
    )
    return ProductResponse.model_validate(upd_product)


@router.put("/be")
async def mark_it_sold(
    is_available: bool,
    product_id: UUID,
    product_handler: "ProductHandler" = Depends(get_product_handler),
):
    upd_product = await product_handler.change_availability(
        product_id=product_id, new_status=is_available
    )
    return ProductResponse.model_validate(upd_product)


@router.delete(
    "/",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_product(
    product_id: UUID,
    product_handler: "ProductHandler" = Depends(get_product_handler),
):
    result = await product_handler.delete_product(product_id=product_id)
    return {"msg": "success"}
