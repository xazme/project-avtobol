from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, status, UploadFile, File
from app.core import settings
from .car_brand_schema import CarBrandCreate, CarBrandUpdate, CarBrandResponse
from .car_brand_dependencies import get_car_brand_handler
from .car_brand_handler import CarSeriesHandler


router = APIRouter(prefix=settings.api.car_brand_prefix, tags=["Car Brand"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CarBrandResponse,
)
async def get_brand(
    car_brand_id: int,
    car_brand_handler: "CarSeriesHandler" = Depends(get_car_brand_handler),
):
    brand = await car_brand_handler.get(id=car_brand_id)
    return CarBrandResponse.model_validate(brand)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=list,
)
async def get_all_brands(
    car_brand_handler: "CarSeriesHandler" = Depends(get_car_brand_handler),
):
    car_brands = await car_brand_handler.get_all()
    return [CarBrandResponse.model_validate(car_brand) for car_brand in car_brands]


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CarBrandResponse,
)
async def create_brand(
    car_brand_data: CarBrandCreate = Depends(),
    car_brand_pic: UploadFile = File(...),
    car_brand_handler: "CarSeriesHandler" = Depends(get_car_brand_handler),
):

    brand = await car_brand_handler.create(
        file=car_brand_pic,
        data=car_brand_data,
    )

    return CarBrandResponse.model_validate(brand)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CarBrandResponse,
)
async def update_brand(
    car_brand_id: int,
    new_car_brand_data: CarBrandUpdate = Depends(),
    car_brand_pic: UploadFile = File(...),
    car_brand_handler: "CarSeriesHandler" = Depends(get_car_brand_handler),
):
    # TODO ПЕРЕДЕЛАТЬ ЛОГИКУ СОЗДАНИЯ
    updated_brand = await car_brand_handler.update(
        id=car_brand_id,
        file=car_brand_pic,
        data=new_car_brand_data,
    )
    return CarBrandResponse.model_validate(updated_brand)


@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
async def delete_brand(
    car_brand_id: int,
    car_brand_handler: "CarSeriesHandler" = Depends(get_car_brand_handler),
):
    await car_brand_handler.delete(id=car_brand_id)
    return {"msg": "success"}
