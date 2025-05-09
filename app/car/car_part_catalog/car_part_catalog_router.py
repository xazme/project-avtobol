from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, status
from app.core import settings
from app.shared import ExceptionRaiser, exec, RouterMode
from .car_part_catalog_schema import (
    CarPartCatalogCreate,
    CarPartCatalogUpdate,
    CarPartCatalogResponse,
)
from .car_part_catalog_dependencies import get_car_part_catalog_service

if TYPE_CHECKING:
    from .car_part_catalog_service import CarPartCatalog

router = APIRouter(
    prefix=settings.api.car_part_catalog_prefix, tags=["Car Part Catalog"]
)


@router.get("/")
async def get_part(
    id: int,
    car_part_catalog_service: "CarPartCatalog" = Depends(get_car_part_catalog_service),
):
    part = await exec(
        mode=RouterMode.GET,
        service=car_part_catalog_service,
        id=id,
    )
    return CarPartCatalogResponse.model_validate(part)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
)
async def get_all_car_parts(
    car_part_catalog_service: "CarPartCatalog" = Depends(get_car_part_catalog_service),
):
    mkm = await exec(
        mode=RouterMode.GET_ALL,
        schema=None,
        service=car_part_catalog_service,
    )
    return [CarPartCatalogResponse.model_validate(item) for item in mkm]


@router.post(
    "/",
    response_model=CarPartCatalogResponse,
    status_code=status.HTTP_200_OK,
)
async def create_part(
    car_brand_info: CarPartCatalogCreate,
    car_part_catalog_service: "CarPartCatalog" = Depends(get_car_part_catalog_service),
):
    part = await exec(
        mode=RouterMode.POST,
        schema=car_brand_info,
        service=car_part_catalog_service,
    )
    return CarPartCatalogResponse.model_validate(part)


@router.put(
    "/",
    response_model=CarPartCatalogResponse,
    status_code=status.HTTP_200_OK,
)
async def update_part(
    car_part_id: int,
    new_car_brand_info: CarPartCatalogUpdate,
    car_part_catalog_service: "CarPartCatalog" = Depends(get_car_part_catalog_service),
):
    part = await exec(
        mode=RouterMode.PUT,
        schema=new_car_brand_info,
        service=car_part_catalog_service,
        id=car_part_id,
    )

    return CarPartCatalogResponse.model_validate(part)


@router.delete(
    "/",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_part(
    car_brand_id: int,
    car_part_catalog_service: "CarPartCatalog" = Depends(get_car_part_catalog_service),
):
    part = await exec(
        id=car_brand_id,
        mode=RouterMode.DELETE,
        schema=None,
        service=car_part_catalog_service,
    )

    return {"msg": "success"}
