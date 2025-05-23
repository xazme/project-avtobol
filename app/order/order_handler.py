from pydantic import BaseModel
from app.cart import CartHandler, Cart
from app.shared import BaseHandler, ExceptionRaiser, OrderStatuses
from .order_repository import OrderRepository


class OrderHandler(BaseHandler):

    def __init__(self, repository: OrderRepository, cart_handler: CartHandler):
        super().__init__(repository)
        self.repository = repository
        self.cart_handler = cart_handler

    async def create_order(
        self,
        user_id: int,
        data: BaseModel,
    ):
        data.model_copy(update={"user_id": user_id, "status": OrderStatuses.OPEN})
        data = data.model_dump(exclude_unset=True)
        order = await self.repository.create_order(data=data)

        if order:
            ExceptionRaiser.raise_exception(status_code=400, detail="уже есть")

        result = await self.cart_handler.delete_position(
            user_id=user_id,
            position_id=data.position_id,
        )

        if not result:
            ExceptionRaiser.raise_exception(
                status_code=400, detail="не удалось удалить позицию"
            )

        return order

    async def create_orders(
        self,
        user_id: int,
        data: BaseModel,
    ):
        positions: list = await self.cart_handler.get_all_positions(user_id=user_id)
        upd_positions = [
            data.model_copy(
                update={"user_id": position.user_id, "product_id": position.product_id},
            )
            for position in positions
        ]

        positions = await self.repository.create_orders(
            positions=upd_positions,
        )

        if not positions:
            ExceptionRaiser.raise_exception(status_code=400, detail="bebe")
        return positions

    async def delete_order(self, user_id: int, order_id: int):
        deleted_order = await self.delete_order(user_id=user_id, order_id=order_id)
        if not deleted_order:
            ExceptionRaiser.raise_exception(status_code=400, detail="pizd")
        else:
            return deleted_order

    async def get_all_orders(self):
        return await self.repository.get_all_orders()

    async def get_user_orders(self, user_id):
        return await self.repository.get_orders(user_id=user_id)

    async def get_active_user_orders(self, user_id: int):
        result = await self.repository.get_active_user_orders(user_id=user_id)
        return result

    async def get_closed_user_orders(self, user_id: int):
        return await self.repository.get_closed_user_orders(user_id=user_id)

    async def get_denied_user_orders(self, user_id):
        return await self.repository.get_denied_user_orders(user_id=user_id)

    async def get_all_active_orders(self):
        return await self.repository.get_all_active_orders()

    async def get_all_closed_orders(self):
        return await self.repository.get_all_closed_orders()

    async def get_all_denied_orders(self):
        return await self.repository.get_all_denied_orders()
