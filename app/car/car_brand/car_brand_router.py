from typing import TYPE_CHECKING, List
from uuid import UUID
from fastapi import (
    APIRouter,
    Depends,
    status,
    Query,
    Path,
    Body,
    Form,
)
from app.core import settings
from .car_brand_schema import (
    CarBrandCreate,
    CarBrandUpdate,
    CarBrandResponse,
)
from .car_brand_dependencies import get_car_brand_handler
from .car_brand_model import CarBrand

if TYPE_CHECKING:
    from .car_brand_handler import CarBrandHandler

router = APIRouter(
    prefix=settings.api.car_brand_prefix,
    tags=["Car Brands"],
)


@router.post(
    "/",
    summary="Create new car brand",
    description="Add a new car brand to the system",
    response_model=CarBrandResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_car_brand(
    car_brand_data: CarBrandCreate = Body(...),
    car_brand_handler: "CarBrandHandler" = Depends(get_car_brand_handler),
) -> CarBrandResponse:

    car_brand: "CarBrand" = await car_brand_handler.create_car_brand(
        car_brand_data=car_brand_data,
    )
    return CarBrandResponse.model_validate(car_brand)


@router.get(
    "/{car_brand_id}",
    summary="Get car brand by ID",
    description="Retrieve detailed information about a specific car brand",
    response_model=CarBrandResponse,
    status_code=status.HTTP_200_OK,
)
async def get_car_brand(
    car_brand_id: UUID = Path(...),
    car_brand_handler: "CarBrandHandler" = Depends(get_car_brand_handler),
) -> CarBrandResponse:
    brand = await car_brand_handler.get_car_brand_by_id(car_brand_id=car_brand_id)
    return CarBrandResponse.model_validate(brand)


@router.get(
    "/",
    summary="Get all car brands",
    description="Retrieve a complete list of all car brands",
    response_model=dict[str, int | None | list[CarBrandResponse]],
    status_code=status.HTTP_200_OK,
)
async def get_all_car_brands(
    search: str = Query(""),
    cursor: int | None = Query(None, gt=0),
    take: int | None = Query(None, gt=0),
    car_brand_handler: "CarBrandHandler" = Depends(get_car_brand_handler),
) -> dict[str, int | None | list[CarBrandResponse]]:
    next_cursor, car_brands = await car_brand_handler.get_all_obj_by_scroll(
        query=search,
        cursor=cursor,
        take=take,
    )
    return {
        "next_cursor": next_cursor if car_brands else None,
        "items": (
            [CarBrandResponse.model_validate(car_brand) for car_brand in car_brands]
        ),
    }


@router.put(
    "/{car_brand_id}",
    summary="Update car brand",
    description="Modify existing car brand information",
    response_model=CarBrandResponse,
    status_code=status.HTTP_200_OK,
)
async def update_car_brand(
    car_brand_id: UUID = Path(...),
    updated_data: CarBrandUpdate = Body(...),
    car_brand_handler: "CarBrandHandler" = Depends(get_car_brand_handler),
) -> CarBrandResponse:
    car_brand = await car_brand_handler.update_car_brand(
        car_brand_id=car_brand_id,
        car_brand_data=updated_data,
    )
    return CarBrandResponse.model_validate(car_brand)


@router.delete(
    "/{car_brand_id}",
    summary="Delete car brand",
    description="Remove a car brand from the system",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
)
async def delete_car_brand(
    car_brand_id: UUID = Path(...),
    car_brand_handler: "CarBrandHandler" = Depends(get_car_brand_handler),
) -> dict[str, str]:
    await car_brand_handler.delete_car_brand(car_brand_id=car_brand_id)
    return {"message": "Успешно удаленно."}
