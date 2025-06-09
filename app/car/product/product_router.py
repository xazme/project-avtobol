from typing import TYPE_CHECKING, Any, Annotated
from uuid import UUID
from fastapi import APIRouter, Body, Depends, status, Query, Path, Form
from app.core import settings
from .product_schema import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    ProductFilters,
)
from .product_dependencies import get_product_handler
from .product_helper import convert_data

if TYPE_CHECKING:
    from .product_handler import ProductHandler

router = APIRouter(
    prefix=settings.api.product,
    tags=["Products"],
)


@router.post(
    "/",
    summary="Create new product",
    description="Add a new product to the catalog",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_data: ProductCreate = Body(...),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> ProductResponse:
    print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
    print(product_data.model_dump(exclude_unset=True))
    product = await product_handler.create_product(product_data=product_data)
    return convert_data(product_data=product)


@router.put(
    "/{product_id}",
    summary="Update product",
    description="Modify existing product information",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
async def update_product(
    product_id: UUID = Path(...),
    new_product_data: ProductUpdate = Depends(ProductUpdate.as_form),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> ProductResponse:

    product = await product_handler.update_product(
        product_id=product_id,
        product_data=new_product_data,
    )
    return convert_data(product_data=product)


@router.get(
    "/{product_id}",
    summary="Get product by ID",
    description="Retrieve detailed information about a specific product",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
async def get_product(
    product_id: UUID = Path(...),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> ProductResponse:
    product = await product_handler.get_product_by_id(product_id=product_id)
    return convert_data(product_data=product)


@router.get(
    "/",
    summary="Get filtered products",
    description="Retrieve paginated list of products with filtering options",
    response_model=dict[str, Any],
    status_code=status.HTTP_200_OK,
)
async def get_all_products(
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0, le=10000),
    filters: ProductFilters = Depends(),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> dict[str, Any]:
    total_count, products = await product_handler.get_all_products(
        page=page,
        page_size=page_size,
        filters=filters,
    )
    return {
        "total_count": total_count,
        "products": convert_data(product_data=products),
    }


@router.patch(
    "/availability",
    summary="Update product availability",
    description="Mark product as available or sold out",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
)
async def update_products_availability(
    products_id: list[UUID] = Body(...),
    is_available: bool = Body(False),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> dict[str, str]:
    await product_handler.bulk_change_availability(
        product_id=products_id,
        new_status=is_available,
    )
    return {
        "message": f"Успешно обновленны статусы для {products_id} на значение {is_available}."
    }


@router.patch(
    "/is_printed",
    summary="Update product printed status",
    description="Mark product as printed or not",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
)
async def update_product_printed_status(
    products_id: list[UUID] = Body(...),
    is_printed: bool = Body(True),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> dict[str, str]:
    await product_handler.bulk_change_printed_status(
        products_id=products_id,
        status=is_printed,
    )
    return {
        "message": f"Успешно обновленны статусы для {products_id} на значение {is_printed}."
    }


@router.delete(
    "/{product_id}",
    summary="Delete product",
    description="Remove product from catalog",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
)
async def delete_product(
    product_id: UUID = Path(...),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> dict[str, str]:
    await product_handler.delete_product(product_id=product_id)
    return {"message": "Успешно удален."}
