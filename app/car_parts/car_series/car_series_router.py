from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, status
from app.core import settings
from app.shared import ExceptionRaiser
from .car_series_schema import CarSeriesUpdate, CarSeriesCreate, CarSeriesResponse
from .car_series_dependencies import get_car_series_service

if TYPE_CHECKING:
    from .car_series_service import CarSeriesService

router = APIRouter(prefix=settings.api.car_brand_prefix, tags=["Car Brand"])


@router.post(
    "/",
    response_model=CarSeriesResponse,
    status_code=status.HTTP_200_OK,
)
async def create_brand(
    car_brand_info: CarSeriesCreate,
    get_car_series_service: "CarSeriesService" = Depends(get_car_series_service),
):

    data = car_brand_info.model_dump()
    brand = await get_car_series_service.create(data=data)
    if not brand:
        ExceptionRaiser.raise_exception(status_code=404, detail="naxyu sgonyai")  # TODO
    return CarSeriesResponse.model_validate(brand)


@router.put(
    "/",
    response_model=CarSeriesResponse,
    status_code=status.HTTP_200_OK,
)
async def update_brand(
    car_brand_id: str,
    new_car_brand_info: CarSeriesUpdate,
    get_car_series_service: "CarSeriesService" = Depends(get_car_series_service),
):
    data = new_car_brand_info.model_dump(exclude_unset=True)
    print(data)
    upd_car_brand_data = await get_car_series_service.update(
        id=car_brand_id, new_data=data
    )
    if not upd_car_brand_data:
        ExceptionRaiser.raise_exception(status_code=404)  # TODO
    return CarSeriesResponse.model_validate(upd_car_brand_data)


@router.delete(
    "/",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_brand(
    car_brand_id: str,
    get_car_series_service: "CarSeriesService" = Depends(get_car_series_service),
):
    result = await get_car_series_service.delete(id=car_brand_id)
    if not result:
        ExceptionRaiser.raise_exception(status_code=404)  # TODO
    return {"msg": "success"}
