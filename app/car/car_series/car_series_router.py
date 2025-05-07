from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, status
from app.core import settings
from app.shared import ExceptionRaiser
from .car_series_schema import CarSeriesUpdate, CarSeriesCreate, CarSeriesResponse
from .car_series_dependencies import get_car_series_service

if TYPE_CHECKING:
    from .car_series_service import CarSeriesService

router = APIRouter(prefix=settings.api.car_series_prefix, tags=["Car Series"])


@router.get("/")
async def get_series(
    id: str,
    car_series_service: "CarSeriesService" = Depends(get_car_series_service),
):
    series = await car_series_service.get(id=id)
    if not series:
        ExceptionRaiser.raise_exception(status_code=404)  # TODO
    return CarSeriesResponse.model_validate(series)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
)
async def get_all_car_series(
    car_series_service: "CarSeriesService" = Depends(get_car_series_service),
):
    car_series = await car_series_service.get_all()
    return car_series


@router.post(
    "/",
    response_model=CarSeriesResponse,
    status_code=status.HTTP_200_OK,
)
async def create_series(
    car_brand_info: CarSeriesCreate,
    car_series_service: "CarSeriesService" = Depends(get_car_series_service),
):
    data = car_brand_info.model_dump()
    print(data)
    series = await car_series_service.create(data=data)
    if not series:
        ExceptionRaiser.raise_exception(status_code=404, detail="naxyu sgonyai")  # TODO
    return CarSeriesResponse.model_validate(series)


@router.put(
    "/",
    response_model=CarSeriesResponse,
    status_code=status.HTTP_200_OK,
)
async def update_series(
    car_brand_id: str,
    new_car_series_info: CarSeriesUpdate,
    car_series_service: "CarSeriesService" = Depends(get_car_series_service),
):
    data = new_car_series_info.model_dump(exclude_unset=True)
    upd_car_series_info = await car_series_service.update(
        id=car_brand_id, new_data=data
    )
    if not upd_car_series_info:
        ExceptionRaiser.raise_exception(status_code=404)  # TODO
    return CarSeriesResponse.model_validate(upd_car_series_info)


@router.delete(
    "/",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_series(
    car_brand_id: str,
    car_series_service: "CarSeriesService" = Depends(get_car_series_service),
):
    result = await car_series_service.delete(id=car_brand_id)
    if not result:
        ExceptionRaiser.raise_exception(status_code=404)  # TODO
    return {"msg": "success"}
