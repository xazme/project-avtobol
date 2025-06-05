from typing import TYPE_CHECKING, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status, File, UploadFile, Query
from app.core import settings
from app.car.car_series import get_car_series_handler
from .product_schema import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    ProductFilters,
)
from .product_dependencies import get_product_handler
from .product_helper import convert_data_for_product, convert_data_for_list_of_products

if TYPE_CHECKING:
    from app.car.car_series import CarSeriesHandler
    from .product_handler import ProductHandler

router = APIRouter(
    prefix=settings.api.product,
    tags=["Products"],
)


@router.post(
    "/",
    summary="Create new product",
    description="Add a new product to the catalog with images",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_data: ProductCreate = Depends(),
    product_pictures: list[UploadFile] = File(
        ...,
        description="Brand logo image file",
        media_type="image/jpeg,image/png",
    ),
    series_handler: "CarSeriesHandler" = Depends(get_car_series_handler),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> ProductResponse:
    await series_handler.check_relation(
        car_brand_id=product_data.car_brand_id,
        car_series_id=product_data.car_series_id,
    )
    product = await product_handler.send_to_queue(
        data=product_data,
        files=product_pictures,
    )
    return {"msg": "в очередь пошла"}
    # return convert_data_for_product(car_part=product)


@router.get(
    "/{product_id}",
    summary="Get product by ID",
    description="Retrieve detailed information about a specific product",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
async def get_product(
    product_id: UUID,
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> ProductResponse:
    product = await product_handler.get_product_by_id(product_id=product_id)
    return convert_data_for_product(car_part=product)


@router.get(
    "/",
    summary="Get filtered products",
    description="Retrieve paginated list of products with filtering options",
    response_model=list[ProductResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_products(
    page: int = Query(1, gt=0, description="Page number starting from 1"),
    page_size: int = Query(10, gt=0, le=100, description="Items per page (max 100)"),
    filters: ProductFilters = Depends(),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> list[ProductResponse]:
    products = await product_handler.get_all_products(
        page=page,
        page_size=page_size,
        filters=filters,
    )
    return convert_data_for_list_of_products(list_of_car_parts=products)


@router.put(
    "/{product_id}",
    summary="Update product",
    description="Modify existing product information and images",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
async def update_product(
    product_id: UUID,
    new_product_data: ProductUpdate = Depends(),
    new_product_pictures: list[UploadFile] | None = File(
        None, description="New product images (optional)"
    ),
    series_handler: "CarSeriesHandler" = Depends(get_car_series_handler),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> ProductResponse:
    await series_handler.check_relation(
        car_brand_id=new_product_data.car_brand_id,
        car_series_id=new_product_data.car_series_id,
    )
    updated_product = await product_handler.update_product(
        id=product_id,
        data=new_product_data,
        files=new_product_pictures,
    )
    return convert_data_for_product(car_part=updated_product)


@router.patch(
    "/{product_id}/availability",
    summary="Update product availability",
    description="Mark product as available or sold out",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
async def update_product_availability(
    product_id: UUID,
    is_available: bool = False,
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> ProductResponse:
    updated_product = await product_handler.change_availability(
        product_id=product_id, new_status=is_available
    )
    return convert_data_for_product(car_part=updated_product)


@router.delete(
    "/{product_id}",
    summary="Delete product",
    description="Remove product from catalog",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_product(
    product_id: UUID,
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> dict[str, str]:
    await product_handler.delete_product(product_id=product_id)
