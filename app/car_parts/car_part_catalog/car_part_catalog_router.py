from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, status
from app.core import settings
from app.shared import ExceptionRaiser
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
    id: str,
    car_part_catalog_service: "CarPartCatalog" = Depends(
        get_car_part_catalog_service,
    ),
):
    part = await car_part_catalog_service.get(id=id)
    if not part:
        ExceptionRaiser.raise_exception(status_code=404)  # TODO
    return CarPartCatalogResponse.model_validate(part)


@router.post(
    "/",
    response_model=CarPartCatalogResponse,
    status_code=status.HTTP_200_OK,
)
async def create_part(
    car_brand_info: CarPartCatalogCreate,
    car_part_catalog_service: "CarPartCatalog" = Depends(get_car_part_catalog_service),
):

    data = car_brand_info.model_dump()
    brand = await car_part_catalog_service.create(data=data)
    if not brand:
        ExceptionRaiser.raise_exception(status_code=404, detail="naxyu sgonyai")  # TODO
    return CarPartCatalogResponse.model_validate(brand)


@router.put(
    "/",
    response_model=CarPartCatalogResponse,
    status_code=status.HTTP_200_OK,
)
async def update_part(
    car_brand_id: str,
    new_car_brand_info: CarPartCatalogUpdate,
    car_part_catalog_service: "CarPartCatalog" = Depends(get_car_part_catalog_service),
):
    data = new_car_brand_info.model_dump(exclude_unset=True)
    print(data)
    upd_car_brand_data = await car_part_catalog_service.update(
        id=car_brand_id, new_data=data
    )
    if not upd_car_brand_data:
        ExceptionRaiser.raise_exception(status_code=404)  # TODO
    return CarPartCatalogResponse.model_validate(upd_car_brand_data)


@router.delete(
    "/",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_part(
    car_brand_id: str,
    car_part_catalog_service: "CarPartCatalog" = Depends(get_car_part_catalog_service),
):
    result = await car_part_catalog_service.delete(id=car_brand_id)
    if not result:
        ExceptionRaiser.raise_exception(status_code=404)  # TODO
    return {"msg": "success"}
