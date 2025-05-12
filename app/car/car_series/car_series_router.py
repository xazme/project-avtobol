from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, status
from app.core import settings
from app.shared import ExceptionRaiser
from .car_series_schema import CarSeriesUpdate, CarSeriesCreate, CarSeriesResponse
from .car_series_dependencies import get_car_series_handler

if TYPE_CHECKING:
    from .car_series_handler import CarSeriesHandler

router = APIRouter(prefix=settings.api.car_series_prefix, tags=["Car Series"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CarSeriesResponse,
)
async def get_series(
    car_series_id: str,
    car_series_handler: "CarSeriesHandler" = Depends(get_car_series_handler),
):
    series = await car_series_handler.get(id=car_series_id)
    return CarSeriesResponse.model_validate(series)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=list,
)
async def get_all_car_series(
    car_series_handler: "CarSeriesHandler" = Depends(get_car_series_handler),
):
    car_series = await car_series_handler.get_all()
    return [CarSeriesResponse(car_serie) for car_serie in car_series]


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CarSeriesResponse,
)
async def create_series(
    car_brand_data: CarSeriesCreate,
    car_series_handler: "CarSeriesHandler" = Depends(get_car_series_handler),
):
    series = await car_series_handler.create(data=car_brand_data)
    return CarSeriesResponse.model_validate(series)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CarSeriesResponse,
)
async def update_series(
    car_series_id: str,
    new_car_series_data: CarSeriesUpdate,
    car_series_handler: "CarSeriesHandler" = Depends(get_car_series_handler),
):
    updated_series = await car_series_handler.update(
        id=car_series_id,
        data=new_car_series_data,
    )
    return CarSeriesResponse.model_validate(updated_series)


@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
async def delete_series(
    car_series_id: str,
    car_series_handler: "CarSeriesHandler" = Depends(get_car_series_handler),
):
    await car_series_handler.delete(id=car_series_id)
    return {"msg": "success"}
