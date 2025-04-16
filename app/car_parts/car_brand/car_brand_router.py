from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends
from app.core import settings
from app.shared import ExceptionRaiser
from .car_brand_schema import CarBrandCreate, CarBrandResponse, CarBrandUpdate
from .car_brand_dependencies import get_car_brand_service

if TYPE_CHECKING:
    from .car_brand_service import CarBrandService

router = APIRouter(prefix=settings.api.car_brand_prefix, tags=["Car Brand"])


@router.post("/")
async def create_brand(
    car_brand_info: CarBrandCreate,
    car_brand_service: "CarBrandService" = Depends(get_car_brand_service),
):

    data = car_brand_info.model_dump()
    brand = await car_brand_service.create(data=data)
    if not brand:
        ExceptionRaiser.raise_exception(status_code=404, detail="naxyu sgonyai")  # TODO
    return CarBrandResponse.model_validate(brand)


@router.put("/")
async def update_brand(
    car_brand_id: int,
    new_car_brand_info: CarBrandUpdate,
    car_brand_service: "CarBrandService" = Depends(get_car_brand_service),
):
    data = new_car_brand_info.model_dump(exclude_unset=True)
    print(data)
    upd_car_brand_data = await car_brand_service.update(id=car_brand_id, new_data=data)
    if not upd_car_brand_data:
        ExceptionRaiser.raise_exception(status_code=404)  # TODO
    return CarBrandResponse.model_validate(upd_car_brand_data)


@router.delete("/")
async def update_brand(
    car_brand_id: int,
    car_brand_service: "CarBrandService" = Depends(get_car_brand_service),
):
    result = await car_brand_service.delete(id=car_brand_id)
    if not result:
        ExceptionRaiser.raise_exception(status_code=404)  # TODO
    return {"msg": "success"}
