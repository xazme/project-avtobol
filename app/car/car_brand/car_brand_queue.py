import base64
from typing import Optional, Any
from faststream import Depends
from app.faststream import broker
from app.database import DBService
from .car_brand_model import CarBrand
from .car_brand_handler import CarBrandHandler
from .car_brand_dependencies import get_car_brand_handler
from .car_brand_schema import CarBrandMessage


@broker.subscriber(queue="brand_input")
async def process_car_brand(
    msg: CarBrandMessage, session=Depends(DBService.get_session)
) -> Optional[CarBrand]:
    car_brand_data = msg.model_dump(exclude_unset=True)
    car_brand_handler: CarBrandHandler = get_car_brand_handler(session=session)
    picture_bytes: bytes = base64.b64decode(s=car_brand_data["picture"])
    filename: str = await car_brand_handler.storage.create_file(picture_bytes)
    car_brand_data.update({"picture": filename})

    print(car_brand_data)

    brand: CarBrand | None = await car_brand_handler.repository.create(
        data=car_brand_data,
    )
    if not brand:
        pass
    print("SUCCESS")
    return brand
