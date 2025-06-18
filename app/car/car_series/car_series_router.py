from typing import TYPE_CHECKING, List
from uuid import UUID
from fastapi import APIRouter, Body, Query, Path, Depends, status
from app.core import settings
from .car_series_schema import (
    CarSeriesUpdate,
    CarSeriesCreate,
    CarSeriesResponse,
)
from .car_series_dependencies import get_car_series_handler

if TYPE_CHECKING:
    from .car_series_handler import CarSeriesHandler

router = APIRouter(
    prefix=settings.api.car_series_prefix,
    tags=["Car Series"],
)


@router.post(
    "/",
    summary="Create new car series",
    description="Add a new car series to the database",
    response_model=CarSeriesResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_car_series(
    series_data: CarSeriesCreate = Body(...),
    car_series_handler: "CarSeriesHandler" = Depends(get_car_series_handler),
) -> CarSeriesResponse:

    series = await car_series_handler.create_series(data=series_data)
    return CarSeriesResponse.model_validate(series)


@router.get(
    "/{car_series_id}",
    summary="Get car series by ID",
    description="Retrieve detailed information about a specific car series",
    response_model=CarSeriesResponse,
    status_code=status.HTTP_200_OK,
)
async def get_car_series(
    car_series_id: UUID = Path(...),
    car_series_handler: "CarSeriesHandler" = Depends(get_car_series_handler),
) -> CarSeriesResponse:
    series = await car_series_handler.get_series_by_id(series_id=car_series_id)
    return CarSeriesResponse.model_validate(series)


@router.get(
    "/",
    summary="Get all car series",
    description="Retrieve a complete list of all car series in the system",
    response_model=List[CarSeriesResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_car_series(
    car_series_handler: "CarSeriesHandler" = Depends(get_car_series_handler),
) -> List[CarSeriesResponse]:
    car_series = await car_series_handler.get_all_series_obj()
    return [CarSeriesResponse.model_validate(series) for series in car_series]


@router.get(
    "/brand/{car_brand_id}",
    summary="Get car series by brand",
    description="Retrieve all car series associated with a specific car brand",
    response_model=List[CarSeriesResponse],
    status_code=status.HTTP_200_OK,
)
async def get_car_series_by_brand(
    car_brand_id: UUID = Path(...),
    car_series_handler: "CarSeriesHandler" = Depends(get_car_series_handler),
) -> List[CarSeriesResponse]:

    car_series = await car_series_handler.get_series_by_car_brand_id(
        car_brand_id=car_brand_id,
    )
    return [CarSeriesResponse.model_validate(series) for series in car_series]


@router.put(
    "/{car_series_id}",
    summary="Update car series",
    description="Modify existing car series information",
    response_model=CarSeriesResponse,
    status_code=status.HTTP_200_OK,
)
async def update_car_series(
    car_series_id: UUID = Path(...),
    updated_data: CarSeriesUpdate = Body(...),
    car_series_handler: "CarSeriesHandler" = Depends(get_car_series_handler),
) -> CarSeriesResponse:
    updated_series = await car_series_handler.update_series(
        car_series_id=car_series_id,
        data=updated_data,
    )
    return CarSeriesResponse.model_validate(updated_series)


@router.delete(
    "/{car_series_id}",
    summary="Delete car series",
    description="Remove a car series from the database",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_car_series(
    car_series_id: UUID = Path(...),
    car_series_handler: "CarSeriesHandler" = Depends(get_car_series_handler),
) -> None:
    await car_series_handler.delete_series(series_id=car_series_id)
