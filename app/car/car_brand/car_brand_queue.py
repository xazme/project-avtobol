import base64
from typing import Optional
from faststream import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.faststream import broker
from app.database import DBService
from app.storage import get_storage_service, StorageService
from .car_brand_model import CarBrand
from .car_brand_handler import CarBrandHandler
from .car_brand_dependencies import get_car_brand_handler
from .car_brand_schema import CarBrandCreateMessage


@broker.subscriber(queue="brand_create")
async def create_car_brand(
    msg: CarBrandCreateMessage,
    session: AsyncSession = Depends(DBService.get_session),
    storage: StorageService = Depends(get_storage_service),
) -> Optional[CarBrand]:
    car_brand_data = msg.model_dump(exclude_unset=True)
    car_brand_handler: CarBrandHandler = get_car_brand_handler(session=session)
    picture_bytes: bytes = base64.b64decode(s=car_brand_data["picture"])
    filename: str = await car_brand_handler.storage.create_file(picture_bytes)
    car_brand_data.update({"picture": filename})
    brand: CarBrand | None = await car_brand_handler.repository.create(
        data=car_brand_data,
    )
    if not brand:
        await storage.delete_file(filename=filename)
        raise Exception
    return brand
