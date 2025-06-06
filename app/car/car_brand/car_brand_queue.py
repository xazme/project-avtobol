import base64
from typing import Optional
from uuid import UUID
from faststream import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.faststream import broker
from app.database import DBService
from app.storage import get_storage_service, StorageService
from .car_brand_model import CarBrand
from .car_brand_handler import CarBrandHandler
from .car_brand_dependencies import get_car_brand_handler
from .car_brand_schema import (
    CarBrandCreateMessage,
    CarBrandUpdateMessage,
    CarBrandCreate,
)


@broker.subscriber(queue="brand_create")
async def create_car_brand(
    msg: CarBrandCreateMessage,
    session: AsyncSession = Depends(DBService.get_session),
) -> None:
    data_to_parse: dict = msg.model_dump(exclude_unset=True)
    car_brand_data: dict = data_to_parse["car_brand_data"]
    file_base64: str = data_to_parse["file"]

    car_brand_handler: CarBrandHandler = get_car_brand_handler(session=session)
    file_bytes: bytes = base64.b64decode(s=file_base64)

    await car_brand_handler.create_car_brand(
        car_brand_data=car_brand_data,
        file=file_bytes,
    )


@broker.subscriber(queue="brand_update")
async def update_car_brand(
    msg: CarBrandUpdateMessage,
    session: AsyncSession = Depends(DBService.get_session),
) -> None:
    data_to_parse: dict = msg.model_dump(exclude_unset=True)
    car_brand_id: UUID = data_to_parse["car_brand_id"]
    car_brand_data: dict = data_to_parse["car_brand_data"]
    file_base64: bytes = data_to_parse.get("file")

    car_brand_handler: CarBrandHandler = get_car_brand_handler(session=session)
    file_bytes: bytes = base64.b64decode(s=file_base64) if file_base64 else None

    await car_brand_handler.update_car_brand(
        car_brand_id=car_brand_id,
        car_brand_data=car_brand_data,
        file=file_bytes,
    )
