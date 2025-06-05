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
) -> Optional[Product]:
    product_data = msg.model_dump(exclude_unset=True)
    product_handler: ProductHandler = get_product_handler(
        session=session, storage=storage
    )

    pictures_bytes = []
    for file in msg.pictures:
        picture_bytes = base64.b64decode(s=file)
        pictures_bytes.append(picture_bytes)

    filenames: str = await product_handler.storage.create_files(
        list_of_files=pictures_bytes
    )

    product_data.update({"pictures": filenames})
    product: Product | None = await product_handler.repository.create(
        data=product_data,
    )
    if not product:
        raise Exception
    return product


@broker.subscriber(queue="product_update")
async def update_product(
    msg: ProductUpdateMessage,
    storage: StorageService = Depends(get_storage_service),
    session: AsyncSession = Depends(DBService.get_session),
) -> Optional[Product]:
    product_id = msg.product_id
    product_data = msg.product_data

    product_handler: ProductHandler = get_product_handler(
        session=session, storage=storage
    )
    old_product: Product = await product_handler.get_product_by_id(product_id)
    old_filenames: list[str] = old_product.pictures

    pictures_bytes = []
    if msg.pictures:
        for file in msg.pictures:
            picture_bytes = base64.b64decode(file)
            pictures_bytes.append(picture_bytes)

        filenames = await product_handler.storage.create_files(
            list_of_files=pictures_bytes
        )

    if filenames:
        product_data.update({"pictures": filenames})

    upd_product: Product | None = await product_handler.repository.update_by_id(
        id=product_id, data=product_data
    )

    if not upd_product:
        raise Exception

    if upd_product:
        await product_handler.storage.delete_files(list_of_files=old_filenames)

    return upd_product
