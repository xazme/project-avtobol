from typing import TYPE_CHECKING, Annotated
from fastapi import APIRouter, Depends, status, Query
from app.core import settings
from app.shared import ExceptionRaiser
from .car_brand_series_schema import (
    CarBrandSeriesCreate,
    CarBrandSeriesResponce,
    CarBrandSeriesUpdate,
)
from .car_brand_series_dependencies import get_brand_series_handler
from .car_brand_series_helper import convert_data_for_car_brand_series_object

if TYPE_CHECKING:
    from .car_brand_series_repository import CarBrandSeriesRepository

router = APIRouter(prefix=settings.api.car_part_prefix, tags=["Car Brand Series"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CarBrandSeriesResponce,
)
async def get_car_part(
    car_brand_series_id: int,
    car_brand_series_handler: "CarBrandSeriesRepository" = Depends(
        get_brand_series_handler
    ),
):
    car_part = await car_brand_series_handler.get(id=car_brand_series_id)
    return CarBrandSeriesResponce.model_validate(car_part)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=list,
)
async def get_all_car_brand_series(
    car_brand_series_handler: "CarBrandSeriesRepository" = Depends(
        get_brand_series_handler
    ),
):
    car_parts = await car_brand_series_handler.get_all()
    return convert_data_for_car_brand_series_object(list_of_car_parts=car_parts)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CarBrandSeriesResponce,
)
async def create_car_part(
    car_part_data: CarBrandSeriesCreate,
    car_brand_series_handler: "CarBrandSeriesRepository" = Depends(
        get_brand_series_handler
    ),
):
    car_part = await car_brand_series_handler.create(data=car_part_data)
    return CarBrandSeriesResponce.model_validate(car_part)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CarBrandSeriesResponce,
)
async def update_car_part(
    car_part_id: int,
    new_car_brand_data: CarBrandSeriesUpdate,
    car_brand_series_handler: "CarBrandSeriesRepository" = Depends(
        get_brand_series_handler,
    ),
):
    upd_car_brand_data = await car_brand_series_handler.update(
        id=car_part_id,
        data=new_car_brand_data,
    )
    return CarBrandSeriesResponce.model_validate(upd_car_brand_data)


@router.delete(
    "/",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_car_part(
    car_brand_series_id: int,
    car_brand_series_handler: "CarBrandSeriesRepository" = Depends(
        get_brand_series_handler,
    ),
):
    result = await car_brand_series_handler.delete(id=car_brand_series_id)

    return {"msg": "success"}
