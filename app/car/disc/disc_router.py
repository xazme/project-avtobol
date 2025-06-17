from typing import TYPE_CHECKING, List
from uuid import UUID
from fastapi import (
    APIRouter,
    Depends,
    status,
    Query,
    Path,
    Body,
)
from app.core import settings
from .disc_schema import DiscBrandCreate, DiscBrandUpdate, DiscBrandResponse
from .disc_dependencies import get_disc_handler
from .disc_model import Disc

if TYPE_CHECKING:
    from .disc_handler import DiscHandler

router = APIRouter(
    prefix=settings.api.disc_prefix,
    tags=["Disc"],
)


@router.post(
    "/",
    summary="Create new disc brand",
    description="Add a new disc brand to the system",
    response_model=DiscBrandResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_disc_brand(
    disc_brand_data: DiscBrandCreate = Body(...),
    disc_brand_handler: "DiscHandler" = Depends(get_disc_handler),
) -> DiscBrandResponse:

    disc_brand = await disc_brand_handler.create_disc_brand(
        disc_brand_data=disc_brand_data,
    )
    return DiscBrandResponse.model_validate(disc_brand)


@router.get(
    "/{disc_brand_id}",
    summary="Get disc brand by ID",
    description="Retrieve detailed information about a specific disc brand",
    response_model=DiscBrandResponse,
    status_code=status.HTTP_200_OK,
)
async def get_disc_brand(
    disc_brand_id: UUID = Path(...),
    disc_brand_handler: "DiscHandler" = Depends(get_disc_handler),
) -> DiscBrandResponse:
    brand = await disc_brand_handler.get_disc_by_id(disc_brand_id=disc_brand_id)
    return DiscBrandResponse.model_validate(brand)


@router.get(
    "/",
    summary="Get all disc brands",
    description="Retrieve a complete list of all disc brands",
    response_model=dict[str, int | None | list[DiscBrandResponse]],
    status_code=status.HTTP_200_OK,
)
async def get_all_disc_brands(
    search: str = Query(""),
    cursor: int | None = Query(None, gt=0),
    take: int | None = Query(None, gt=0),
    disc_brand_handler: "DiscHandler" = Depends(get_disc_handler),
) -> dict[str, int | None | list[DiscBrandResponse]]:
    next_cursor, disc_brands = await disc_brand_handler.get_all_obj_by_scroll(
        query=search,
        cursor=cursor,
        take=take,
    )
    return {
        "next_cursor": next_cursor if disc_brands else None,
        "items": (
            [DiscBrandResponse.model_validate(disc_brand) for disc_brand in disc_brands]
        ),
    }


@router.put(
    "/{disc_brand_id}",
    summary="Update disc brand",
    description="Modify existing disc brand information",
    response_model=DiscBrandResponse,
    status_code=status.HTTP_200_OK,
)
async def update_disc_brand(
    disc_brand_id: UUID = Path(...),
    updated_data: DiscBrandUpdate = Body(...),
    disc_brand_handler: "DiscHandler" = Depends(get_disc_handler),
) -> DiscBrandResponse:
    disc_brand = await disc_brand_handler.update_disc_brand(
        disc_brand_id=disc_brand_id,
        disc_brand_data=updated_data,
    )
    return DiscBrandResponse.model_validate(disc_brand)


@router.delete(
    "/{disc_brand_id}",
    summary="Delete disc brand",
    description="Remove a disc brand from the system",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
)
async def delete_disc_brand(
    disc_brand_id: UUID = Path(...),
    disc_brand_handler: "DiscHandler" = Depends(get_disc_handler),
) -> dict[str, str]:
    await disc_brand_handler.delete_disc_brand(disc_brand_id=disc_brand_id)
    return {"message": "Успешно удалено."}
