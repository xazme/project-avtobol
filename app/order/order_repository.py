from uuid import UUID
from sqlalchemy import Select, Insert, Result, and_, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.shared import BaseCRUD
from app.car.product import Product
from .order_model import Order
from .order_enums import OrderStatuses


class OrderRepository(BaseCRUD):

    def __init__(self, session: AsyncSession, model: Order):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: Order = model

    async def get_all_orders_by_user_id(
        self,
        user_id: UUID,
        status: OrderStatuses,
    ) -> list[Order]:
        stmt: Select = (
            Select(self.model)
            .where(
                and_(
                    self.model.user_id == user_id,
                    self.model.status == status,
                )
            )
            .options(
                selectinload(self.model.user),
                selectinload(self.model.product).joinedload(Product.car_brand),
                selectinload(self.model.product).joinedload(Product.car_series),
                selectinload(self.model.product).joinedload(Product.car_part),
            )
            .order_by(self.model.created_at)
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_all_orders_by_phone_number(
        self,
        phone_number: str,
    ) -> list[Order]:
        stmt: Select = (
            Select(self.model)
            .where(
                and_(
                    self.model.user_phone == phone_number,
                )
            )
            .options(
                selectinload(self.model.user),
                selectinload(self.model.product).joinedload(Product.car_brand),
                selectinload(self.model.product).joinedload(Product.car_series),
                selectinload(self.model.product).joinedload(Product.car_part),
            )
            .order_by(self.model.created_at)
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_all_orders(
        self,
        page: int,
        page_size: int,
        status: OrderStatuses,
    ) -> list[Order]:
        stmt: Select = (
            Select(self.model)
            .options(
                selectinload(self.model.user),
                selectinload(self.model.product).joinedload(Product.car_brand),
                selectinload(self.model.product).joinedload(Product.car_series),
                selectinload(self.model.product).joinedload(Product.car_part),
            )
            .limit(limit=page_size)
            .offset((page - 1) * page_size)
            .order_by(self.model.created_at)
            .where(self.model.status == status)
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_all_orders_by_scroll(
        self,
        query: str,
        cursor: int | None,
        take: int | None,
        status: OrderStatuses,
    ) -> tuple[int | None, list]:
        cursor = cursor if cursor is not None else 0
        subq = (
            Select(Product.id).where(Product.article.ilike(f"%{query}%"))
        ).subquery()

        stmt_count: Select = Select(func.count(self.model.id)).where(
            and_(
                self.model.product_id.in_(Select(subq.c.id)),
                self.model.status == status,
            )
        )
        stmt: Select = (
            Select(self.model)
            .options(
                selectinload(self.model.user),
                selectinload(self.model.product),
                selectinload(self.model.product).joinedload(Product.car_brand),
                selectinload(self.model.product).joinedload(Product.car_series),
                selectinload(self.model.product).joinedload(Product.car_part),
            )
            .order_by(self.model.created_at)
            .offset(cursor)
            .where(
                and_(
                    self.model.product_id.in_(Select(subq.c.id)),
                    self.model.status == status,
                )
            )
        )

        if take is not None:
            stmt = stmt.limit(take)

        result: Result = await self.session.execute(statement=stmt)
        result_count: Result = await self.session.execute(statement=stmt_count)
        count = result_count.scalar()

        next_cursor = (
            cursor + take if take is not None and (cursor + take) <= count else None
        )

        return next_cursor, result.scalars().all()

    async def change_order_status(
        self,
        order_id: UUID,
        status: OrderStatuses,
    ) -> Order | None:
        order: Order | None = await self.get_by_id(id=order_id)
        try:
            if order:
                order.status = status
                await self.session.commit()
                await self.session.refresh(order)
                return order
        except IntegrityError:
            await self.session.rollback()

        return None

    async def create_orders(
        self,
        list_of_products: list[dict],
    ) -> list["Order"] | None:
        try:
            stmt = Insert(self.model).returning(self.model.id)

            result = await self.session.execute(stmt, list_of_products)
            inserted_ids = [row.id for row in result.fetchall()]

            await self.session.commit()

            query = (
                Select(self.model)
                .where(self.model.id.in_(inserted_ids))
                .options(
                    selectinload(self.model.user),
                    selectinload(self.model.product).selectinload(Product.car_brand),
                    selectinload(self.model.product).selectinload(Product.car_series),
                    selectinload(self.model.product).selectinload(Product.car_part),
                )
            )

            refetched = await self.session.execute(query)
            return refetched.scalars().all()

        except IntegrityError:
            await self.session.rollback()
            return None
