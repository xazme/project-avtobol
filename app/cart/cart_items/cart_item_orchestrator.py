from uuid import UUID
from app.shared import ExceptionRaiser
from app.car.product import Product, ProductHandler
from .cart_item_model import CartItem
from .cart_item_schema import CartAddItem, CartDeleteItem
from .cart_item_handler import CartItemHandler
from ..cart.cart_handler import CartHandler
from ..cart.cart_model import Cart


class CartItemOrchestrator:

    def __init__(
        self,
        product_handler: ProductHandler,
        cart_handler: CartHandler,
        cart_item_handler: CartItemHandler,
    ):
        self.product_handler: ProductHandler = product_handler
        self.cart_item_handler: CartItemHandler = cart_item_handler
        self.cart_handler: CartHandler = cart_handler

    async def add_item(
        self,
        user_id: UUID,
        data: CartAddItem,
    ) -> CartItem | None:
        user_cart_id: "Cart" = await self.cart_handler.get_user_cart_id(user_id=user_id)
        product = await self.product_handler.get_product_by_id(data.product_id)

        if product.is_available != True:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail="Продукт недоступен.",
            )
        product_in_the_cart: CartItem = (
            await self.cart_item_handler.repository.get_cart_item_position(
                cart_id=user_cart_id,
                product_id=data.product_id,
            )
        )

        if product_in_the_cart:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Данный товар уже существует в вашей корзине.",
            )

        cart_data = data.model_dump(exclude_unset=True)
        cart_data.update({"cart_id": user_cart_id})

        cart_item: CartItem = await self.cart_item_handler.create_obj(data=cart_data)
        return cart_item

    async def delete_item(
        self,
        user_id,
        data: CartDeleteItem,
    ) -> None:
        user_cart_id: UUID | None = (
            await self.cart_handler.repository.get_user_cart_id_by_user_id(
                user_id=user_id,
            )
        )

        if not user_cart_id:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Корзина пользователя не найдена",
            )

        product_in_the_cart: CartItem = (
            await self.cart_item_handler.repository.get_cart_item_position(
                cart_id=user_cart_id, product_id=data.product_id
            )
        )

        if not product_in_the_cart:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Данный товар не найден в вашей корзине.",
            )

        cart_data = data.model_dump(exclude_unset=True)
        cart_data.update({"cart_id": user_cart_id})

        await self.cart_item_handler.repository.delete_item(**cart_data)

    async def clear_cart(
        self,
        user_id: UUID,
    ) -> None:
        user_cart_id = await self.cart_handler.get_user_cart_id(user_id=user_id)
        await self.cart_item_handler.repository.clear_user_cart(cart_id=user_cart_id)

    async def get_user_cart(
        self,
        user_id: UUID,
    ):
        user_cart_id: UUID = await self.cart_handler.get_user_cart_id(
            user_id=user_id,
        )
        user_cart: list[CartItem] = (
            await self.cart_item_handler.repository.get_all_user_positions(
                cart_id=user_cart_id
            )
        )
        return user_cart
