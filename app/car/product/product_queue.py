import base64
from uuid import UUID
from typing import Optional
from faststream import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.faststream import broker
from app.database import DBService
from app.storage import get_storage_service, StorageService
from .product_model import Product
from .product_handler import ProductHandler
from .product_dependencies import get_product_handler
from .product_schema import ProductCreateMessage, ProductUpdateMessage


@broker.subscriber(queue="product_create")
async def create_product(
    msg: ProductCreateMessage,
    storage: StorageService = Depends(get_storage_service),
    session: AsyncSession = Depends(DBService.get_session),
) -> None:
    data_to_parse = msg.model_dump(exclude_unset=True)
    product_data = data_to_parse["product_data"]
    files = data_to_parse["files"]

    product_handler: ProductHandler = get_product_handler(
        session=session, storage=storage
    )

    files_bytes = []
    for file in files:
        file_bytes: bytes = base64.b64decode(s=file)
        files_bytes.append(file_bytes)

    await product_handler.create_product(product_data=product_data, files=files_bytes)


@broker.subscriber(queue="product_update")
async def update_product(
    msg: ProductUpdateMessage,
    storage: StorageService = Depends(get_storage_service),
    session: AsyncSession = Depends(DBService.get_session),
) -> Optional[Product]:
    data_to_parse: dict = msg.model_dump(exclude_unset=True)
    product_id: UUID = data_to_parse["product_id"]
    product_data: dict = data_to_parse["product_data"]
    files: list[bytes] = data_to_parse.get("files")

    product_handler: ProductHandler = get_product_handler(
        session=session, storage=storage
    )

    files_bytes = [base64.b64decode(file) for file in files] if files else None

    if files:
        files_bytes: list[bytes] = []
        for file in files:
            file_bytes: bytes = base64.b64decode(file)
            files_bytes.append(file_bytes)

    await product_handler.update_product(
        product_id=product_id,
        new_data=product_data,
        files=files_bytes,
    )
