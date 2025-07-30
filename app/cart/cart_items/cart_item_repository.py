from uuid import UUID
from sqlalchemy import Select, Delete, Result
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from app.car.product.product_model import Product
from .cart_item_model import CartItem


class CartItemRepository(BaseCRUD):

    def __init__(self, session: AsyncSession, model: CartItem):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: CartItem = model

    async def delete_item(
        self,
        cart_id: UUID,
        product_id: UUID,
    ) -> None:
        stmt = Delete(self.model).where(
            self.model.cart_id == cart_id,
            self.model.product_id == product_id,
        )
        result: Result = await self.session.execute(statement=stmt)
        await self.session.commit()

    async def clear_user_cart(
        self,
        cart_id: UUID,
    ) -> None:
        stmt = Delete(self.model).where(self.model.cart_id == cart_id)
        result: Result = await self.session.execute(statement=stmt)
        await self.session.commit()

    async def get_cart_item_position(
        self,
        cart_id: UUID,
        product_id: UUID,
    ) -> CartItem | None:
        stmt = Select(self.model).where(
            self.model.cart_id == cart_id,
            self.model.product_id == product_id,
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_all_user_positions(self, cart_id: UUID) -> list[CartItem]:
        stmt = (
            Select(self.model)
            .where(self.model.cart_id == cart_id)
            .options(selectinload(self.model.product).selectinload(Product.car_brand))
            .options(selectinload(self.model.product).selectinload(Product.car_series))
            .options(selectinload(self.model.product).selectinload(Product.car_part))
            .options(selectinload(self.model.product).selectinload(Product.tire))
            .options(selectinload(self.model.product).selectinload(Product.disc))
            .options(selectinload(self.model.product).selectinload(Product.engine))
        )

        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()
