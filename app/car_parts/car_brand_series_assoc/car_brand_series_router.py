from typing import TYPE_CHECKING, Annotated
from fastapi import APIRouter, Depends, status, Query
from app.core import settings
from app.shared import ExceptionRaiser
from .car_brand_series_schema import CarPartCreate, CarPartResponce, CarPartUpdate
from .car_brand_series_dependencies import get_car_part_service

if TYPE_CHECKING:
    from .car_brand_series_service import CarBrandSeriesService

router = APIRouter(prefix=settings.api.car_part_prefix, tags=["Car Brand Series"])


@router.get("/")
async def get_car_part(
    id: Annotated[int, Query()],
    car_part_service: "CarBrandSeriesService" = Depends(get_car_part_service),
):
    brand = await car_part_service.get(id=id)
    if not brand:
        ExceptionRaiser.raise_exception(status_code=404)  # TODO
    return CarPartResponce.model_validate(brand)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
)
async def get_all_car_brand_series(
    car_part_service: "CarBrandSeriesService" = Depends(get_car_part_service),
):
    car_parts = await car_part_service.get_all()
    return car_parts


@router.post(
    "/",
    # response_model=CarBrandResponse,
    status_code=status.HTTP_200_OK,
)
async def create_car_part(
    car_part_info: CarPartCreate,
    car_part_service: "CarBrandSeriesService" = Depends(get_car_part_service),
):

    data = car_part_info.model_dump()
    brand = await car_part_service.create(data=data)
    if not brand:
        ExceptionRaiser.raise_exception(status_code=404, detail="naxyu sgonyai")  # TODO
    # return CarPartResponce.model_validate(brand)


@router.put(
    "/",
    # response_model=CarBrandResponse,
    status_code=status.HTTP_200_OK,
)
async def update_car_part(
    car_part_id: int,
    new_car_brand_info: CarPartUpdate,
    car_part_service: "CarBrandSeriesService" = Depends(get_car_part_service),
):
    data = new_car_brand_info.model_dump(exclude_unset=True)
    upd_car_brand_data = await car_part_service.update(id=car_part_id, new_data=data)
    if not upd_car_brand_data:
        ExceptionRaiser.raise_exception(status_code=404)  # TODO
    return CarPartResponce.model_validate(upd_car_brand_data)


@router.delete(
    "/",
    # response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_car_part(
    car_part_id: int,
    car_part_service: "CarBrandSeriesService" = Depends(get_car_part_service),
):
    result = await car_part_service.delete(id=car_part_id)
    if not result:
        ExceptionRaiser.raise_exception(status_code=404)  # TODO
    return {"msg": "success"}
