from typing import TYPE_CHECKING, List
from uuid import UUID
from fastapi import (
    APIRouter,
    Depends,
    status,
    UploadFile,
    File,
    Body,
    Query,
    Path,
    Form,
)
from app.core import settings
from .car_brand_schema import (
    CarBrandCreate,
    CarBrandUpdate,
    CarBrandResponse,
)
from .car_brand_dependencies import get_car_brand_handler

if TYPE_CHECKING:
    from .car_brand_handler import CarBrandHandler

router = APIRouter(
    prefix=settings.api.car_brand_prefix,
    tags=["Car Brands"],
)


@router.post(
    "/",
    summary="Create new car brand",
    description="Add a new car brand to the system",
    response_model=dict[str, str],
    status_code=status.HTTP_201_CREATED,
)
async def create_car_brand(
    brand_data: CarBrandCreate = Form(...),
    brand_logo: UploadFile = File(...),
    car_brand_handler: "CarBrandHandler" = Depends(get_car_brand_handler),
) -> dict[str, str]:
    print("s")
    await car_brand_handler.send_to_queue_for_create(
        file=brand_logo,
        data=brand_data,
    )
    return {"message": "Добавлено в очередь для создания."}


@router.get(
    "/{car_brand_id}",
    summary="Get car brand by ID",
    description="Retrieve detailed information about a specific car brand",
    response_model=CarBrandResponse,
    status_code=status.HTTP_200_OK,
)
async def get_car_brand(
    car_brand_id: UUID = Path(...),
    car_brand_handler: "CarBrandHandler" = Depends(get_car_brand_handler),
) -> CarBrandResponse:
    brand = await car_brand_handler.get_car_brand_by_id(car_brand_id=car_brand_id)
    return CarBrandResponse.model_validate(brand)


@router.get(
    "/",
    summary="Get all car brands",
    description="Retrieve a complete list of all car brands",
    response_model=List[CarBrandResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_car_brands(
    query: str = Query(""),
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0, le=100),
    car_brand_handler: "CarBrandHandler" = Depends(get_car_brand_handler),
) -> List[CarBrandResponse]:
    car_brands = await car_brand_handler.get_all_brands(
        query=query,
        page=page,
        page_size=page_size,
    )
    return [CarBrandResponse.model_validate(brand) for brand in car_brands]


@router.put(
    "/{car_brand_id}",
    summary="Update car brand",
    description="Modify existing car brand information",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
)
async def update_car_brand(
    car_brand_id: UUID = Path(...),
    updated_data: CarBrandUpdate = Depends(),
    brand_logo: UploadFile | None = File(None),
    car_brand_handler: "CarBrandHandler" = Depends(get_car_brand_handler),
) -> dict[str, str]:
    await car_brand_handler.send_to_queue_for_update(
        car_brand_id=car_brand_id,
        file=brand_logo,
        data=updated_data,
    )
    return {"message": "Добавлено в очередь для обновления."}


@router.delete(
    "/{car_brand_id}",
    summary="Delete car brand",
    description="Remove a car brand from the system",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
)
async def delete_car_brand(
    car_brand_id: UUID = Path(...),
    car_brand_handler: "CarBrandHandler" = Depends(get_car_brand_handler),
) -> dict[str, str]:
    await car_brand_handler.delete_car_brand(car_brand_id=car_brand_id)
    return {"message": "Успешно удаленно."}
