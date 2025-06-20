from typing import TYPE_CHECKING
from uuid import UUID
from fastapi import APIRouter, Depends, status, Body, Query
from app.core import settings
from .car_part_catalog_schema import (
    CarPartCreate,
    CarPartUpdate,
    CarPartResponse,
)
from .car_part_catalog_dependencies import get_car_part_handler

if TYPE_CHECKING:
    from .car_part_catalog_handler import CarPartHandler

router = APIRouter(
    prefix=settings.api.car_part_prefix,
    tags=["Car Part"],
)


@router.post(
    "/",
    summary="Create new car part",
    description="Add a new car part to the catalog",
    response_model=CarPartResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_car_part(
    car_part_data: CarPartCreate = Body(...),
    car_part_catalog_handler: "CarPartHandler" = Depends(get_car_part_handler),
) -> CarPartResponse:
    new_part = await car_part_catalog_handler.create_part(data=car_part_data)
    return CarPartResponse.model_validate(new_part)


@router.get(
    "/",
    summary="Get all car parts",
    description="Retrieve a complete list of all car parts in the catalog",
    response_model=dict[str, int | None | list[CarPartResponse]],
    status_code=status.HTTP_200_OK,
)
async def get_all_car_parts(
    search: str = Query(""),
    cursor: int | None = Query(None, gt=-1),
    take: int | None = Query(None, ge=0),
    car_part_catalog_handler: "CarPartHandler" = Depends(get_car_part_handler),
) -> dict[str, int | None | list[CarPartResponse]]:
    next_cursor, parts = await car_part_catalog_handler.get_all_parts(
        query=search,
        cursor=cursor,
        take=take,
    )
    return {
        "next_cursor": next_cursor if parts else None,
        "items": ([CarPartResponse.model_validate(part) for part in parts]),
    }


@router.get(
    "/{car_part_id}",
    summary="Get car part by ID",
    description="Retrieve detailed information about a specific car part",
    response_model=CarPartResponse,
    status_code=status.HTTP_200_OK,
)
async def get_car_p2art(
    car_part_id: UUID,
    car_part_catalog_handler: "CarPartHandler" = Depends(get_car_part_handler),
) -> CarPartResponse:
    part = await car_part_catalog_handler.get_part_by_id(car_part_id=car_part_id)
    return CarPartResponse.model_validate(part)


@router.put(
    "/{car_part_id}",
    summary="Update car part",
    description="Modify existing car part information",
    response_model=CarPartResponse,
    status_code=status.HTTP_200_OK,
)
async def update_car_part(
    car_part_id: UUID,
    updated_data: CarPartUpdate,
    car_part_catalog_handler: "CarPartHandler" = Depends(get_car_part_handler),
) -> CarPartResponse:
    updated_part = await car_part_catalog_handler.update_part(
        car_part_id=car_part_id,
        data=updated_data,
    )
    return CarPartResponse.model_validate(updated_part)


@router.delete(
    "/{car_part_id}",
    summary="Delete car part",
    description="Remove a car part from the catalog",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_car_part(
    car_part_id: UUID,
    car_part_catalog_handler: "CarPartHandler" = Depends(get_car_part_handler),
) -> None:
    await car_part_catalog_handler.delete_part(car_part_id=car_part_id)
