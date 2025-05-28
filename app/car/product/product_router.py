from typing import TYPE_CHECKING
from uuid import UUID
from fastapi import APIRouter, Depends, status, File, UploadFile
from app.core import settings
from app.car.car_series import get_car_series_handler
from .product_schema import (
    ProductCreate,
    ProductResponce,
    ProductUpdate,
)
from .product_dependencies import get_product_handler
from .product_helper import convert_data_for_product

if TYPE_CHECKING:
    from app.car.car_series import CarSeriesHandler
    from .product_handler import ProductHandler

router = APIRouter(prefix=settings.api.product, tags=["Product"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponce,
)
async def get_product(
    product_id: UUID,
    product_handler: "ProductHandler" = Depends(get_product_handler),
):
    product = await product_handler.get_product_by_id(product_id=product_id)
    return ProductResponce.model_validate(product)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=list,
)
async def get_all_products(
    page: int,
    page_size: int,
    product_handler: "ProductHandler" = Depends(get_product_handler),
):
    products = await product_handler.get_all_products(
        page=page,
        page_size=page_size,
    )
    return convert_data_for_product(list_of_car_parts=products)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponce,
)
async def create_product(
    product_data: ProductCreate = Depends(),
    product_pictures: list[UploadFile] = File(...),
    series_handler: "CarSeriesHandler" = Depends(get_car_series_handler),
    product_handler: "ProductHandler" = Depends(get_product_handler),
):
    await series_handler.check_relation(
        brand_id=product_data.brand_id,
        series_id=product_data.series_id,
    )
    car_part = await product_handler.create_product(
        data=product_data,
        files=product_pictures,
    )
    return ProductResponce.model_validate(car_part)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponce,
)
async def update_product(
    product_id: UUID,
    new_product_data: ProductUpdate = Depends(),
    new_product_pictures: list[UploadFile] | None = File(...),
    series_handler: "CarSeriesHandler" = Depends(get_car_series_handler),
    product_handler: "ProductHandler" = Depends(get_product_handler),
):
    await series_handler.check_relation(
        brand_id=new_product_data.brand_id,
        series_id=new_product_data.series_id,
    )
    upd_product = await product_handler.update_product(
        id=product_id,
        data=new_product_data,
        files=new_product_pictures,
    )
    return ProductResponce.model_validate(upd_product)


@router.put("/be")
async def mark_it_sold(
    is_available: bool,
    product_id: UUID,
    product_handler: "ProductHandler" = Depends(get_product_handler),
):
    upd_product = await product_handler.change_availability(
        product_id=product_id, new_status=is_available
    )
    return ProductResponce.model_validate(upd_product)


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
