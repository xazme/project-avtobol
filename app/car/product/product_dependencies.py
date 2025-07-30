from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from app.storage import get_storage_handler, StorageHandler
from .product_model import Product
from .product_repository import ProductRepository
from .product_handler import ProductHandler
from .product_orchestrator import ProductOrchestrator
from ..disc.disc import DiscHandler, get_disc_handler
from ..tire.tire import TireHandler, get_tire_handler
from ..engine import EngineHandler, get_engine_handler


def get_product_handler(
    session: AsyncSession = Depends(DBService.get_session),
) -> ProductHandler:
    repository = ProductRepository(
        session=session,
        model=Product,
    )
    return ProductHandler(repository=repository)


def get_product_orchestrator(
    product_handler: ProductHandler = Depends(get_product_handler),
    disc_handler: DiscHandler = Depends(get_disc_handler),
    tire_handler: TireHandler = Depends(get_tire_handler),
    engine_handler: EngineHandler = Depends(get_engine_handler),
    storage_handler: StorageHandler = Depends(get_storage_handler),
) -> ProductOrchestrator:
    return ProductOrchestrator(
        product_handler=product_handler,
        disc_handler=disc_handler,
        tire_handler=tire_handler,
        engine_handler=engine_handler,
        storage_handler=storage_handler,
    )
