from typing import Optional
from uuid import UUID
from app.shared import BaseHandler, ExceptionRaiser
from .cart_repository import CartRepository
from .cart_model import Cart


class CartHandler(BaseHandler):
    def __init__(self, repository: CartRepository):
        super().__init__(repository)
        self.repository: CartRepository = repository

    async def get_all_user_positions(
        self,
        user_id: UUID,
    ) -> list[Cart]:
        return await self.repository.get_all_user_positions(user_id=user_id)

    async def create_position(
        self,
        user_id: UUID,
        product_id: UUID,
    ) -> Optional[Cart]:
        obj: dict | None = await self.repository.create_position(
            user_id=user_id,
            product_id=product_id,
        )
        if not obj:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Такого продукта больше не существует, либо он в вашей корзине.",
            )
        return obj

    async def delete_position(
        self,
        user_id: UUID,
        product_id: UUID,
    ) -> bool:
        result: bool = await self.repository.delete_position(
            user_id=user_id,
            product_id=product_id,
        )
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail=f"Неудалось удалить позицию {product_id}.",
            )
        return result

    async def delete_all_positions(
        self,
        user_id: UUID,
    ) -> bool:
        result: bool = await self.repository.delete_all_positions(user_id=user_id)
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=404, detail="Корзина пуста, нечего удалять."
            )
        return result
