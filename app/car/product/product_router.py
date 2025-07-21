from typing import TYPE_CHECKING, Any, Annotated
from uuid import UUID
from fastapi import APIRouter, Body, Depends, status, Query, Path, UploadFile, File
from app.auth.auth_guard import required_roles
from app.user.user_enums import UserRoles
from app.core import settings
from ..tire.tire import TireFiltersPublic, TireFiltersPrivate
from ..disc.disc import DiscFiltersPublic, DiscFiltersPrivate
from ..engine import EngineFilters
from .product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductResponsePublic,
    ProductResponsePrivate,
    ProductFiltersPublic,
    ProductFiltersPrivate,
)
from .product_handler import ProductHandler
from .product_orchestrator import ProductOrchestrator
from .product_dependencies import get_product_handler, get_product_orchestrator
from .product_helper import (
    convert_product_data_public,
    convert_product_data_private,
    convert_product_data_basic,
)

if TYPE_CHECKING:
    from app.user import User


router = APIRouter(
    prefix=settings.api.product,
    tags=["Products"],
)


@router.get(
    "/private",
    summary="Get filtered products (private)",
    description="Retrieve paginated list of products with filtering options in private mode",
    response_model=dict[str, int | None | list[ProductResponsePrivate]],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(required_roles([UserRoles.WORKER]))],
)
async def get_all_products_private(
    cursor: int | None = Query(None, gt=-1),
    take: int | None = Query(None, gt=0),
    product_filters: ProductFiltersPrivate = Depends(),
    tire_filters: TireFiltersPrivate = Depends(),
    disc_filters: DiscFiltersPrivate = Depends(),
    engine_filters: EngineFilters = Depends(),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> dict[str, int | None | list[ProductResponsePrivate]]:
    next_cursor, total_count, products = (
        await product_handler.get_all_products_by_cursor(
            cursor=cursor,
            take=take,
            product_filters=product_filters,
            tire_filters=tire_filters,
            disc_filters=disc_filters,
            engine_filters=engine_filters,
        )
    )

    return {
        "next_cursor": next_cursor,
        "total_count": total_count,
        "items": convert_product_data_private(product_data=products),
    }


@router.get(
    "/public",
    summary="Get filtered products. Public mode",
    description="Retrieve paginated list of products with filtering options",
    response_model=dict[str, int | None | list[ProductResponsePublic]],
    status_code=status.HTTP_200_OK,
)
async def get_all_products_public(
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0, le=10000),
    product_filters: ProductFiltersPublic = Depends(),
    tire_filters: TireFiltersPublic = Depends(),
    disc_filters: DiscFiltersPublic = Depends(),
    engine_filters: EngineFilters = Depends(),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> dict[int | None | list[ProductResponsePublic]]:
    total_count, products = await product_handler.get_all_products_by_page(
        page=page,
        page_size=page_size,
        product_filters=product_filters,
        tire_filters=tire_filters,
        disc_filters=disc_filters,
        engine_filters=engine_filters,
    )

    return {
        "total_count": total_count,
        "items": convert_product_data_public(product_data=products),
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
    await product_handler.bulk_update_availability(
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
    await product_handler.bulk_update_printed_status(
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
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(
    product_id: UUID = Path(...),
    product_orchestrator: ProductOrchestrator = Depends(get_product_orchestrator),
) -> None:
    await product_orchestrator.delete_product(product_id=product_id)


@router.post(
    "/",
    summary="Create new product",
    description="Add a new product to the catalog",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_pictures: list[UploadFile] = File(...),
    product_data: ProductCreate = Body(...),
    user: "User" = Depends(required_roles(allowed_roles=[UserRoles.WORKER])),
    product_orchestrator: ProductOrchestrator = Depends(get_product_orchestrator),
) -> ProductResponse:
    product = await product_orchestrator.create_product(
        user_id=user.id,
        product_data=product_data,
        files=product_pictures,
    )
    return convert_product_data_basic(
        product_data=product,
    )


@router.put(
    "/{product_id}",
    summary="Update product",
    description="Modify existing product information",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
async def update_product(
    product_id: UUID = Path(...),
    removed_photos: list[str] = Body(...),
    new_product_data: ProductUpdate = Body(...),
    new_product_pictures: list[UploadFile] | None = File(None),
    user: "User" = Depends(required_roles(allowed_roles=[UserRoles.WORKER])),
    product_orchestrator: ProductOrchestrator = Depends(get_product_orchestrator),
) -> ProductResponse:

    product = await product_orchestrator.update_product(
        user_id=user.id,
        product_id=product_id,
        product_data=new_product_data,
        files=new_product_pictures,
        removed_photos=removed_photos,
    )

    return convert_product_data_basic(
        product_data=product,
    )


@router.get(
    "/{product_id}",
    summary="Get product by ID",
    description="Retrieve detailed information about a specific product",
    response_model=ProductResponsePublic,
    status_code=status.HTTP_200_OK,
)
async def get_product(
    product_id: UUID = Path(...),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> ProductResponsePublic:
    product = await product_handler.get_product_by_id(product_id=product_id)
    return convert_product_data_public(product_data=product)


@router.get(
    "/private/{product_id}",
    summary="Get product by ID. Worker Access",
    description="Retrieve detailed information about a specific product",
    response_model=ProductResponsePrivate,
    dependencies=[Depends(required_roles([UserRoles.WORKER]))],
    status_code=status.HTTP_200_OK,
)
async def get_product(
    product_id: UUID = Path(...),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> ProductResponsePrivate:
    product = await product_handler.get_product_by_id(product_id=product_id)
    return convert_product_data_private(product_data=product)


@router.get(
    "/article/{article}",
    summary="Get product by article",
    description="Retrieve detailed information about a specific product",
    response_model=ProductFiltersPublic,
    status_code=status.HTTP_200_OK,
)
async def get_product_by_article(
    article: str = Path(...),
    product_handler: "ProductHandler" = Depends(get_product_handler),
) -> ProductFiltersPublic:
    product = await product_handler.get_product_by_article(article=article)
    return convert_product_data_public(product_data=product)
