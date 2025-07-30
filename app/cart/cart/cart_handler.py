from typing import Optional
from uuid import UUID
from app.shared import BaseHandler, ExceptionRaiser
from .cart_repository import CartRepository
from .cart_model import Cart


class CartHandler(BaseHandler):
    def __init__(self, repository: CartRepository):
        super().__init__(repository)
        self.repository: CartRepository = repository

    async def get_user_cart_id(
        self,
        user_id: UUID,
    ) -> Optional[UUID]:
        user_cart_id: "UUID" | None = await self.repository.get_user_cart_id_by_user_id(
            user_id=user_id,
        )
        if not user_cart_id:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="У пользователя отсутствует корзина. Вероятнее всего пользователя несуществует. ",
            )
        return user_cart_id

    async def get_user_cart(
        self,
        user_id: UUID,
    ) -> Optional["Cart"]:
        user_cart: "Cart" | None = await self.repository.get_user_cart_by_user_id(
            user_id=user_id,
        )
        if not user_cart:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="У пользователя отсутствует корзина. Вероятнее всего пользователя несуществует. ",
            )
        return user_cart
