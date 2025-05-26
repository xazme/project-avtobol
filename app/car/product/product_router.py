from typing import TYPE_CHECKING
from uuid import UUID
from fastapi import APIRouter, Depends, status, File, UploadFile, BackgroundTasks
from app.core import settings
from .product_schema import (
    ProductCreate,
    ProductResponce,
    ProductUpdate,
)
from .product_dependencies import get_product_handler
from .product_helper import convert_data_for_product

if TYPE_CHECKING:
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
    product = await product_handler.get_product_by_id(id=product_id)
    return ProductResponce.model_validate(product)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=list,
)
async def get_all_products(
    product_handler: "ProductHandler" = Depends(get_product_handler),
):
    # TODO
    products = await product_handler.get_all_products()
    return convert_data_for_product(list_of_car_parts=products)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponce,
)
async def create_product(
    product_data: ProductCreate = Depends(),
    product_pictures: list[UploadFile] = File(...),
    product_handler: "ProductHandler" = Depends(get_product_handler),
):
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
    product_id: int,
    new_product_data: ProductUpdate,
    product_handler: "ProductHandler" = Depends(get_product_handler),
):
    upd_product = await product_handler.update_product(
        id=product_id,
        data=new_product_data,
    )
    return ProductResponce.model_validate(upd_product)


@router.delete(
    "/",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_product(
    product_id: int,
    product_handler: "ProductHandler" = Depends(get_product_handler),
):
    result = await product_handler.delete_product(id=product_id)

    return {"msg": "success"}
