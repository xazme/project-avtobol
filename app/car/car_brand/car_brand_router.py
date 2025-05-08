from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from app.core import settings
from app.shared import ExceptionRaiser
from app.storage import get_storage_service
from .car_brand_schema import CarBrandCreate, CarBrandResponse, CarBrandUpdate
from .car_brand_dependencies import get_car_brand_service

if TYPE_CHECKING:
    from app.storage import StorageService
    from .car_brand_service import CarBrandService

router = APIRouter(prefix=settings.api.car_brand_prefix, tags=["Car Brand"])


@router.get("/")
async def get_brand(
    id: int,
    car_brand_service: "CarBrandService" = Depends(get_car_brand_service),
):
    brand = await car_brand_service.get(id=id)
    if not brand:
        ExceptionRaiser.raise_exception(status_code=404)  # TODO
    return CarBrandResponse.model_validate(brand)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
)
async def get_all_car_brands(
    car_brand_service: "CarBrandService" = Depends(get_car_brand_service),
):
    car_brands = await car_brand_service.get_all()
    return car_brands


@router.post(
    "/",
    response_model=CarBrandResponse,
    status_code=status.HTTP_200_OK,
)
async def create_brand(
    car_brand_info: CarBrandCreate = Depends(),
    car_brand_pic: UploadFile = File(...),
    storage_service: "StorageService" = Depends(get_storage_service),
    car_brand_service: "CarBrandService" = Depends(get_car_brand_service),
):
    filename = await storage_service.create_file(file=car_brand_pic)
    car_brand_upd = car_brand_info.model_copy()
    car_brand_upd.picture = filename
    data = car_brand_upd.model_dump()

    brand = await car_brand_service.create(data=data)
    if not brand:
        await storage_service.delete_file(filename=filename)
        ExceptionRaiser.raise_exception(status_code=404, detail="naxyu sgonyai")  # TODO

    # return {"msg": "sss"}

    return CarBrandResponse.model_validate(brand)


@router.put(
    "/",
    response_model=CarBrandResponse,
    status_code=status.HTTP_200_OK,
)
async def update_brand(
    car_brand_id: int,
    new_car_brand_info: CarBrandUpdate,
    car_brand_service: "CarBrandService" = Depends(get_car_brand_service),
):
    data = new_car_brand_info.model_dump(exclude_unset=True)
    upd_car_brand_data = await car_brand_service.update(id=car_brand_id, new_data=data)
    if not upd_car_brand_data:
        ExceptionRaiser.raise_exception(status_code=404)  # TODO
    return CarBrandResponse.model_validate(upd_car_brand_data)


@router.delete(
    "/",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_brand(
    car_brand_id: int,
    car_brand_service: "CarBrandService" = Depends(get_car_brand_service),
):
    result = await car_brand_service.delete(id=car_brand_id)
    if not result:
        ExceptionRaiser.raise_exception(status_code=404)  # TODO
    return {"msg": "success"}
