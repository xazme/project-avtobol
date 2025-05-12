# from typing import TYPE_CHECKING, Annotated
# from fastapi import APIRouter, Depends, status, Query
# from app.core import settings
# from app.shared import ExceptionRaiser
# from .car_brand_series_schema import (
#     CarBrandSeriesCreate,
#     CarBrandSeriesResponce,
#     CarBrandSeriesUpdate,
# )
# from .car_brand_series_dependencies import get_car_part_service
# from .car_brand_series_helprer import convert_data_for_car_brand_series_object

# if TYPE_CHECKING:
#     from .car_brand_series_service import CarBrandSeriesService

# router = APIRouter(prefix=settings.api.car_part_prefix, tags=["Car Brand Series"])


# @router.get("/")
# async def get_car_part(
#     id: Annotated[int, Query()],
#     car_part_service: "CarBrandSeriesService" = Depends(get_car_part_service),
# ):
#     car_part = await car_part_service.get(id=id)
#     if not car_part:
#         ExceptionRaiser.raise_exception(status_code=404)  # TODO
#     return CarBrandSeriesResponce.model_validate(car_part)


# @router.get(
#     "/all",
#     status_code=status.HTTP_200_OK,
# )
# async def get_all_car_brand_series(
#     car_part_service: "CarBrandSeriesService" = Depends(get_car_part_service),
# ):
#     car_parts = await car_part_service.get_all()
#     return convert_data_for_car_brand_series_object(list_of_car_parts=car_parts)


# @router.post(
#     "/",
#     response_model=CarBrandSeriesResponce,
#     status_code=status.HTTP_200_OK,
# )
# async def create_car_part(
#     car_part_info: CarBrandSeriesCreate,
#     car_part_service: "CarBrandSeriesService" = Depends(get_car_part_service),
# ):

#     data = car_part_info.model_dump()
#     car_part = await car_part_service.create(data=data)
#     if not car_part:
#         ExceptionRaiser.raise_exception(status_code=404, detail="naxyu sgonyai")  # TODO
#     return CarBrandSeriesResponce.model_validate(car_part)


# @router.put(
#     "/",
#     response_model=CarBrandSeriesResponce,
#     status_code=status.HTTP_200_OK,
# )
# async def update_car_part(
#     car_part_id: int,
#     new_car_brand_info: CarBrandSeriesUpdate,
#     car_part_service: "CarBrandSeriesService" = Depends(get_car_part_service),
# ):
#     data = new_car_brand_info.model_dump(exclude_unset=True)
#     upd_car_brand_data = await car_part_service.update(id=car_part_id, new_data=data)
#     if not upd_car_brand_data:
#         ExceptionRaiser.raise_exception(status_code=404)  # TODO
#     return CarBrandSeriesResponce.model_validate(upd_car_brand_data)


# @router.delete(
#     "/",
#     response_model=None,
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# async def delete_car_part(
#     car_part_id: int,
#     car_part_service: "CarBrandSeriesService" = Depends(get_car_part_service),
# ):
#     result = await car_part_service.delete(id=car_part_id)
#     if not result:
#         ExceptionRaiser.raise_exception(status_code=404)  # TODO
#     return
