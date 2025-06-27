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
from .tire_schema import TiresBrandCreate, TiresBrandUpdate, TiresBrandResponse
from .tire_dependencies import get_tires_handler
from .tire_model import TireBrand
from .tire_handler import TiresHandler

router = APIRouter(
    prefix=settings.api.tires_prefix,
    tags=["Tire Brand"],
)


@router.post(
    "/",
    summary="Create new tires brand",
    description="Add a new tires brand to the system",
    response_model=TiresBrandResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tires_brand(
    tire_brand_data: TiresBrandCreate = Body(...),
    tire_brand_handler: "TiresHandler" = Depends(get_tires_handler),
) -> TiresBrandResponse:

    tire_brand: "TireBrand" = await tire_brand_handler.create_tire_brand(
        tire_brand_data=tire_brand_data,
    )
    return TiresBrandResponse.model_validate(tire_brand)


@router.get(
    "/{tire_brand_id}",
    summary="Get tires brand by ID",
    description="Retrieve detailed information about a specific tires brand",
    response_model=TiresBrandResponse,
    status_code=status.HTTP_200_OK,
)
async def get_tires_brand(
    tire_brand_id: UUID = Path(...),
    tire_brand_handler: "TiresHandler" = Depends(get_tires_handler),
) -> TiresBrandResponse:
    tire_brand = await tire_brand_handler.get_tire_by_id(tire_brand_id=tire_brand_id)
    return TiresBrandResponse.model_validate(tire_brand)


@router.get(
    "/",
    summary="Get all tires brands",
    description="Retrieve a complete list of all tires brands",
    response_model=dict[str, int | None | list[TiresBrandResponse]],
    status_code=status.HTTP_200_OK,
)
async def get_all_tires_brands(
    search: str = Query(""),
    cursor: int | None = Query(None, gt=-1),
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
    "/{tire_brand_id}",
    summary="Update tires brand",
    description="Modify existing tires brand information",
    response_model=TiresBrandResponse,
    status_code=status.HTTP_200_OK,
)
async def update_tires_brand(
    tire_brand_id: UUID = Path(...),
    updated_data: TiresBrandUpdate = Body(...),
    tire_brand_handler: "TiresHandler" = Depends(get_tires_handler),
) -> TiresBrandResponse:
    tire_brand = await tire_brand_handler.update_tire_brand(
        tire_brand_id=tire_brand_id,
        tire_brand_data=updated_data,
    )
    return TiresBrandResponse.model_validate(tire_brand)


@router.delete(
    "/{tire_brand_id}",
    summary="Delete tires brand",
    description="Remove a tires brand from the system",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_tires_brand(
    tire_brand_id: UUID = Path(...),
    tire_brand_handler: "TiresHandler" = Depends(get_tires_handler),
) -> None:
    await tire_brand_handler.delete_tire_brand(tires_brand_id=tire_brand_id)
