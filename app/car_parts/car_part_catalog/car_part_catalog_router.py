from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, status
from app.core import settings
from app.shared import ExceptionRaiser
from .car_part_catalog_schema import (
    CarPartCatalogCreate,
    CarPartCatalogUpdate,
    CarPartCatalogResponse,
)
from .car_part_caralog_dependencies import get_car_series_service

if TYPE_CHECKING:
    from .car_part_catalog_service import CarPartCatalog

router = APIRouter(
    prefix=settings.api.car_part_catalog_prefix, tags=["Car Part Catalog"]
)


@router.post(
    "/",
    response_model=CarPartCatalogResponse,
    status_code=status.HTTP_200_OK,
)
async def create_series(
    car_brand_info: CarPartCatalogCreate,
    get_car_series_service: "CarPartCatalog" = Depends(get_car_series_service),
):

    data = car_brand_info.model_dump()
    brand = await get_car_series_service.create(data=data)
    if not brand:
        ExceptionRaiser.raise_exception(status_code=404, detail="naxyu sgonyai")  # TODO
    return CarPartCatalogResponse.model_validate(brand)


@router.put(
    "/",
    response_model=CarPartCatalogResponse,
    status_code=status.HTTP_200_OK,
)
async def update_series(
    car_brand_id: str,
    new_car_brand_info: CarPartCatalogUpdate,
    get_car_series_service: "CarPartCatalog" = Depends(get_car_series_service),
):
    data = new_car_brand_info.model_dump(exclude_unset=True)
    print(data)
    upd_car_brand_data = await get_car_series_service.update(
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
async def delete_series(
    car_brand_id: str,
    get_car_series_service: "CarPartCatalog" = Depends(get_car_series_service),
):
    result = await get_car_series_service.delete(id=car_brand_id)
    if not result:
        ExceptionRaiser.raise_exception(status_code=404)  # TODO
    return {"msg": "success"}
