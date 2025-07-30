from typing import TYPE_CHECKING
from uuid import UUID
from fastapi import APIRouter, Depends, status, Query, Path, Body
from app.core import settings
from .disc_brand_schema import DiscBrandCreate, DiscBrandUpdate, DiscBrandResponse
from .disc_brand_dependencies import get_disc_brand_handler

if TYPE_CHECKING:
    from .disc_brand_handler import DiscBrandHandler

router = APIRouter(
    prefix=settings.api.disc_brand_prefix,
    tags=["Disc Brand"],
)


@router.post(
    "/",
    summary="Create new disc brand",
    response_model=DiscBrandResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_disc_brand(
    data: DiscBrandCreate = Body(...),
    handler: "DiscBrandHandler" = Depends(get_disc_brand_handler),
) -> DiscBrandResponse:
    brand = await handler.create_obj(data)
    return DiscBrandResponse.model_validate(brand)


@router.get(
    "/{disc_brand_id}",
    summary="Get disc brand by ID",
    response_model=DiscBrandResponse,
)
async def get_disc_brand_by_id(
    disc_brand_id: UUID = Path(...),
    handler: "DiscBrandHandler" = Depends(get_disc_brand_handler),
) -> DiscBrandResponse:
    brand = await handler.get_obj_by_id(disc_brand_id)
    return DiscBrandResponse.model_validate(brand)


@router.get(
    "/",
    summary="Get all disc brands (with search & scroll)",
    response_model=dict[str, int | None | list[DiscBrandResponse]],
)
async def get_all_disc_brands(
    search: str = Query(""),
    cursor: int | None = Query(None, gt=-1),
    take: int | None = Query(None, gt=0),
    handler: "DiscBrandHandler" = Depends(get_disc_brand_handler),
) -> dict[str, int | None | list[DiscBrandResponse]]:
    next_cursor, items = await handler.get_all_obj_by_scroll(
        query=search,
        cursor=cursor,
        take=take,
    )
    return {
        "next_cursor": next_cursor,
        "items": [DiscBrandResponse.model_validate(i) for i in items],
    }


@router.put(
    "/{disc_brand_id}",
    summary="Update disc brand",
    response_model=DiscBrandResponse,
)
async def update_disc_brand(
    disc_brand_id: UUID = Path(...),
    data: DiscBrandUpdate = Body(...),
    handler: "DiscBrandHandler" = Depends(get_disc_brand_handler),
) -> DiscBrandResponse:
    brand = await handler.update_obj(id=disc_brand_id, data=data)
    return DiscBrandResponse.model_validate(brand)


@router.delete(
    "/{disc_brand_id}",
    summary="Delete disc brand",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_disc_brand(
    disc_brand_id: UUID = Path(...),
    handler: "DiscBrandHandler" = Depends(get_disc_brand_handler),
) -> None:
    await handler.delete_obj(id=disc_brand_id)
