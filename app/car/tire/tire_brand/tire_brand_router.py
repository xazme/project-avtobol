from typing import TYPE_CHECKING
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
from .tire_brand_schema import TireBrandCreate, TireBrandUpdate, TireBrandResponse
from .tire_brand_dependencies import get_tire_brand_handler

if TYPE_CHECKING:
    from .tire_brand_handler import TireBrandHandler


router = APIRouter(
    prefix=settings.api.tire_brand_prefix,
    tags=["Tire Brand"],
)


@router.post(
    "/",
    summary="Create new tire brand",
    response_model=TireBrandResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tire_brand(
    data: TireBrandCreate = Body(...),
    handler: "TireBrandHandler" = Depends(get_tire_brand_handler),
) -> TireBrandResponse:
    tire_brand = await handler.create_obj(data)
    return TireBrandResponse.model_validate(tire_brand)


@router.get(
    "/{tire_brand_id}",
    summary="Get tire brand by ID",
    response_model=TireBrandResponse,
)
async def get_tire_brand_by_id(
    tire_brand_id: UUID = Path(...),
    handler: "TireBrandHandler" = Depends(get_tire_brand_handler),
) -> TireBrandResponse:
    brand = await handler.get_obj_by_id(tire_brand_id)
    return TireBrandResponse.model_validate(brand)


@router.get(
    "/",
    summary="Get all tire brands",
    response_model=dict[str, int | None | list[TireBrandResponse]],
)
async def get_all_tire_brands(
    search: str = Query(""),
    cursor: int | None = Query(None, gt=-1),
    take: int | None = Query(None, gt=0),
    handler: "TireBrandHandler" = Depends(get_tire_brand_handler),
) -> dict[str, int | None | list[TireBrandResponse]]:
    next_cursor, items = await handler.get_all_obj_by_scroll(
        query=search,
        cursor=cursor,
        take=take,
    )
    return {
        "next_cursor": next_cursor,
        "items": [TireBrandResponse.model_validate(i) for i in items],
    }


@router.put(
    "/{tire_brand_id}",
    summary="Update tire brand",
    response_model=TireBrandResponse,
)
async def update_tire_brand(
    tire_brand_id: UUID = Path(...),
    data: TireBrandUpdate = Body(...),
    handler: "TireBrandHandler" = Depends(get_tire_brand_handler),
) -> TireBrandResponse:
    brand = await handler.update_obj(id=tire_brand_id, data=data)
    return TireBrandResponse.model_validate(brand)


@router.delete(
    "/{tire_brand_id}",
    summary="Delete tire brand",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_tire_brand(
    tire_brand_id: UUID = Path(...),
    handler: "TireBrandHandler" = Depends(get_tire_brand_handler),
) -> None:
    await handler.delete_obj(id=tire_brand_id)
