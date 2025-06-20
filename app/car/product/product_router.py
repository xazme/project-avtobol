from typing import TYPE_CHECKING, Any, Annotated
from uuid import UUID
from fastapi import APIRouter, Body, Depends, status, Query, Path, Form
from app.auth import requied_roles
from app.user import UserRoles
from app.core import settings
from .product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductFilters,
    ProductFiltersExtended,
    ProductResponse,
    ProductResponseExtend,
)
from .product_dependencies import get_product_handler
from .product_helper import convert_data

if TYPE_CHECKING:
    from app.user import User
    from .product_handler import ProductHandler

router = APIRouter(
    prefix=settings.api.product,
    tags=["Products"],
)


@router.get(
    "/pub",
    summary="Get filtered products. Private mode",
    description="Retrieve paginated list of products with filtering options",
    response_model=dict[str, Any],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(requied_roles([UserRoles.WORKER]))],
)
async def get_all_products_private(
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0, le=10000),
    filters: ProductFiltersExtended = Depends(),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> dict[str, Any]:
    total_count, products = await product_handler.get_all_products(
        is_private=True,
        page=page,
        page_size=page_size,
        filters=filters,
    )
    return {
        "total_count": total_count,
        "items": convert_data(
            product_data=products,
            is_private=True,
        ),
    }


@router.get(
    "/priv",
    summary="Get filtered products. Public mode",
    description="Retrieve paginated list of products with filtering options",
    response_model=dict[str, Any],
    status_code=status.HTTP_200_OK,
)
async def get_all_products_public(
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0, le=10000),
    filters: ProductFilters = Depends(),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> dict[str, Any]:
    total_count, products = await product_handler.get_all_products(
        is_private=False,
        page=page,
        page_size=page_size,
        filters=filters,
    )
    return {
        "total_count": total_count,
        "items": convert_data(product_data=products),
    }


@router.patch(
    "/toggle_availible_status",
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
        products_id=products_id,
        new_status=is_available,
    )
    return {
        "message": f"Успешно обновленны статусы для {products_id} на значение {is_available}."
    }


@router.patch(
    "/toggle_printed_status",
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
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_product(
    product_id: UUID = Path(...),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> None:
    await product_handler.delete_product(product_id=product_id)


@router.post(
    "/",
    summary="Create new product",
    description="Add a new product to the catalog",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_data: ProductCreate = Body(...),
    user: "User" = Depends(requied_roles(allowed_roles=[UserRoles.WORKER])),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> ProductResponse:
    product = await product_handler.create_product(
        user_id=user.id,
        product_data=product_data,
    )
    return ProductResponse.model_validate(product)


@router.put(
    "/{product_id}",
    summary="Update product",
    description="Modify existing product information",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
async def update_product(
    product_id: UUID = Path(...),
    new_product_data: ProductUpdate = Body(...),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> ProductResponse:

    product = await product_handler.update_product(
        product_id=product_id,
        product_data=new_product_data,
    )

    return ProductResponse.model_validate(product)


@router.get(
    "/{product_id}",
    summary="Get product by ID",
    description="Retrieve detailed information about a specific product",
    response_model=ProductResponseExtend,
    status_code=status.HTTP_200_OK,
)
async def get_product(
    product_id: UUID = Path(...),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> ProductResponseExtend:
    product = await product_handler.get_product_by_id(product_id=product_id)
    return convert_data(product_data=product)
