from typing import TYPE_CHECKING, List
from uuid import UUID
from fastapi import APIRouter, Depends, status, UploadFile, File, Body
from app.core import settings
from .car_brand_schema import (
    CarBrandCreate,
    CarBrandUpdate,
    CarBrandResponse,
)
from .car_brand_dependencies import get_car_brand_handler

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
    response_model=dict[str, str],
    status_code=status.HTTP_201_CREATED,
)
async def create_car_brand(
    brand_data: CarBrandCreate = Depends(),
    brand_logo: UploadFile = File(
        ...,
        description="Brand logo image file",
        media_type="image/jpeg,image/png",
    ),
    car_brand_handler: "CarBrandHandler" = Depends(get_car_brand_handler),
) -> dict[str, str]:
    await car_brand_handler.send_to_queue_for_create(
        file=brand_logo,
        data=brand_data,
    )
    return {"msg": "Добавлено в очередь для создания"}


@router.get(
    "/{car_brand_id}",
    summary="Get car brand by ID",
    description="Retrieve detailed information about a specific car brand",
    response_model=CarBrandResponse,
    status_code=status.HTTP_200_OK,
)
async def get_car_brand(
    car_brand_id: UUID,
    car_brand_handler: "CarBrandHandler" = Depends(get_car_brand_handler),
) -> CarBrandResponse:
    brand = await car_brand_handler.get_car_brand_by_id(car_brand_id=car_brand_id)
    return CarBrandResponse.model_validate(brand)


@router.get(
    "/",
    summary="Get all car brands",
    description="Retrieve a complete list of all car brands",
    response_model=List[CarBrandResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_car_brands(
    car_brand_handler: "CarBrandHandler" = Depends(get_car_brand_handler),
) -> List[CarBrandResponse]:
    car_brands = await car_brand_handler.get_all_brands()
    return [CarBrandResponse.model_validate(brand) for brand in car_brands]


@router.put(
    "/{car_brand_id}",
    summary="Update car brand",
    description="Modify existing car brand information",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
)
async def update_car_brand(
    car_brand_id: UUID,
    updated_data: CarBrandUpdate = Depends(),
    brand_logo: UploadFile | None = File(None),
    car_brand_handler: "CarBrandHandler" = Depends(get_car_brand_handler),
) -> dict[str, str]:
    await car_brand_handler.send_to_queue_for_update(
        car_brand_id=car_brand_id,
        file=brand_logo,
        data=updated_data,
    )
    return {"msg": "Добавлено в очередь для обновления"}


@router.delete(
    "/{car_brand_id}",
    summary="Delete car brand",
    description="Remove a car brand from the system",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_car_brand(
    car_brand_id: UUID,
    car_brand_handler: "CarBrandHandler" = Depends(get_car_brand_handler),
) -> dict[str, str]:
    await car_brand_handler.delete_car_brand(car_brand_id=car_brand_id)
