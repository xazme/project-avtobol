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
from .tires_schema import TiresBrandCreate, TiresBrandUpdate, TiresBrandResponse
from .tires_dependencies import get_tires_handler
from .tires_model import Tires
from .tires_handler import TiresHandler

router = APIRouter(
    prefix=settings.api.tires_prefix,
    tags=["Tires"],
)


@router.post(
    "/",
    summary="Create new tires brand",
    description="Add a new tires brand to the system",
    response_model=TiresBrandResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tires_brand(
    tires_brand_data: TiresBrandCreate = Body(...),
    tires_brand_handler: "TiresHandler" = Depends(get_tires_handler),
) -> TiresBrandResponse:

    tires_brand: "Tires" = await tires_brand_handler.create_tires_brand(
        data=tires_brand_data,
    )
    return TiresBrandResponse.model_validate(tires_brand)


@router.get(
    "/{tires_brand_id}",
    summary="Get tires brand by ID",
    description="Retrieve detailed information about a specific tires brand",
    response_model=TiresBrandResponse,
    status_code=status.HTTP_200_OK,
)
async def get_tires_brand(
    tires_brand_id: UUID = Path(...),
    tires_brand_handler: "TiresHandler" = Depends(get_tires_handler),
) -> TiresBrandResponse:
    brand = await tires_brand_handler.get_tires_by_id(tires_brand_id=tires_brand_id)
    return TiresBrandResponse.model_validate(brand)


@router.get(
    "/",
    summary="Get all tires brands",
    description="Retrieve a complete list of all tires brands",
    response_model=dict[str, int | None | list[TiresBrandResponse]],
    status_code=status.HTTP_200_OK,
)
async def get_all_tires_brands(
    search: str = Query(""),
    cursor: int | None = Query(None, gt=0),
    take: int | None = Query(None, gt=0),
    tires_brand_handler: "TiresHandler" = Depends(get_tires_handler),
) -> dict[str, int | None | list[TiresBrandResponse]]:
    next_cursor, tires_brands = await tires_brand_handler.get_all_obj_by_scroll(
        query=search,
        cursor=cursor,
        take=take,
    )
    return {
        "next_cursor": next_cursor if tires_brands else None,
        "items": (
            [
                TiresBrandResponse.model_validate(tires_brand)
                for tires_brand in tires_brands
            ]
        ),
    }


@router.put(
    "/{tires_brand_id}",
    summary="Update tires brand",
    description="Modify existing tires brand information",
    response_model=TiresBrandResponse,
    status_code=status.HTTP_200_OK,
)
async def update_tires_brand(
    tires_brand_id: UUID = Path(...),
    updated_data: TiresBrandUpdate = Body(...),
    tires_brand_handler: "TiresHandler" = Depends(get_tires_handler),
) -> TiresBrandResponse:
    tires_brand = await tires_brand_handler.update_tires_brand(
        tires_brand_id=tires_brand_id,
        data=updated_data,
    )
    return TiresBrandResponse.model_validate(tires_brand)


@router.delete(
    "/{tires_brand_id}",
    summary="Delete tires brand",
    description="Remove a tires brand from the system",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
)
async def delete_tires_brand(
    tires_brand_id: UUID = Path(...),
    tires_brand_handler: "TiresHandler" = Depends(get_tires_handler),
) -> dict[str, str]:
    await tires_brand_handler.delete_tires_brand(tires_brand_id=tires_brand_id)
    return {"message": "Успешно удалено."}
