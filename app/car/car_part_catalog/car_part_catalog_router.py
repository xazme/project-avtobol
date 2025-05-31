from typing import TYPE_CHECKING, List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.core import settings
from .car_part_catalog_schema import (
    CarPartCatalogCreate,
    CarPartCatalogUpdate,
    CarPartCatalogResponse,
)
from .car_part_catalog_dependencies import get_car_part_catalog_handler

if TYPE_CHECKING:
    from .car_part_catalog_handler import CarPartCatalogHandler

router = APIRouter(
    prefix=settings.api.car_part_catalog_prefix,
    tags=["Car Part Catalog"],
)


@router.post(
    "/",
    summary="Create new car part",
    description="Add a new car part to the catalog",
    response_model=CarPartCatalogResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_car_part(
    car_part_data: CarPartCatalogCreate,
    car_part_catalog_handler: "CarPartCatalogHandler" = Depends(
        get_car_part_catalog_handler
    ),
) -> CarPartCatalogResponse:
    new_part = await car_part_catalog_handler.create_part(data=car_part_data)
    return CarPartCatalogResponse.model_validate(new_part)


@router.get(
    "/{car_part_id}",
    summary="Get car part by ID",
    description="Retrieve detailed information about a specific car part",
    response_model=CarPartCatalogResponse,
    status_code=status.HTTP_200_OK,
)
async def get_car_part(
    car_part_id: UUID,
    car_part_catalog_handler: "CarPartCatalogHandler" = Depends(
        get_car_part_catalog_handler
    ),
) -> CarPartCatalogResponse:
    part = await car_part_catalog_handler.get_part_by_id(car_part_id=car_part_id)
    return CarPartCatalogResponse.model_validate(part)


@router.get(
    "/",
    summary="Get all car parts",
    description="Retrieve a complete list of all car parts in the catalog",
    response_model=List[CarPartCatalogResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_car_parts(
    car_part_catalog_handler: "CarPartCatalogHandler" = Depends(
        get_car_part_catalog_handler
    ),
) -> List[CarPartCatalogResponse]:
    parts = await car_part_catalog_handler.get_all_parts()
    return [CarPartCatalogResponse.model_validate(part) for part in parts]


@router.put(
    "/{car_part_id}",
    summary="Update car part",
    description="Modify existing car part information",
    response_model=CarPartCatalogResponse,
    status_code=status.HTTP_200_OK,
)
async def update_car_part(
    car_part_id: UUID,
    updated_data: CarPartCatalogUpdate,
    car_part_catalog_handler: "CarPartCatalogHandler" = Depends(
        get_car_part_catalog_handler
    ),
) -> CarPartCatalogResponse:
    updated_part = await car_part_catalog_handler.update_part(
        car_part_id=car_part_id,
        data=updated_data,
    )
    return CarPartCatalogResponse.model_validate(updated_part)


@router.delete(
    "/{car_part_id}",
    summary="Delete car part",
    description="Remove a car part from the catalog",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_car_part(
    car_part_id: UUID,
    car_part_catalog_handler: "CarPartCatalogHandler" = Depends(
        get_car_part_catalog_handler
    ),
) -> dict[str, str]:
    await car_part_catalog_handler.delete_part(car_part_id=car_part_id)
