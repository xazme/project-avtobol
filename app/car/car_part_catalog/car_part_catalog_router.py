from typing import TYPE_CHECKING
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
    prefix=settings.api.car_part_catalog_prefix, tags=["Car Part Catalog"]
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CarPartCatalogResponse,
)
async def get_part(
    car_part_id: UUID,
    car_part_catalog_handler: "CarPartCatalogHandler" = Depends(
        get_car_part_catalog_handler,
    ),
):
    part = await car_part_catalog_handler.get_part_by_id(id=car_part_id)
    return CarPartCatalogResponse.model_validate(part)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=list[CarPartCatalogResponse],
)
async def get_all_parts(
    car_part_catalog_handler: "CarPartCatalogHandler" = Depends(
        get_car_part_catalog_handler
    ),
):
    parts = await car_part_catalog_handler.get_all_parts()
    return [CarPartCatalogResponse.model_validate(item) for item in parts]


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CarPartCatalogResponse,
)
async def create_part(
    car_part_data: CarPartCatalogCreate,
    car_part_catalog_handler: "CarPartCatalogHandler" = Depends(
        get_car_part_catalog_handler
    ),
):
    new_part = await car_part_catalog_handler.create_part(data=car_part_data)
    return CarPartCatalogResponse.model_validate(new_part)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CarPartCatalogResponse,
)
async def update_part(
    car_part_id: UUID,
    new_car_part_data: CarPartCatalogUpdate,
    car_part_catalog_handler: "CarPartCatalogHandler" = Depends(
        get_car_part_catalog_handler
    ),
):
    updated_part = await car_part_catalog_handler.update_part(
        id=car_part_id,
        data=new_car_part_data,
    )

    return CarPartCatalogResponse.model_validate(updated_part)


@router.delete(
    "/",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_part(
    car_part_id: UUID,
    car_part_catalog_handler: "CarPartCatalogHandler" = Depends(
        get_car_part_catalog_handler
    ),
):
    await car_part_catalog_handler.delete_part(id=car_part_id)
    return {"msg": "success"}
