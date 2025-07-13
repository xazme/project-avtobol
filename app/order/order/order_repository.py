from uuid import UUID
from sqlalchemy import Select, Result, func, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from .order_model import Order
from .order_schema import OrderFiltersCompressed, OrderFilters
from .order_enums import OrderStatuses


class OrderRepository(BaseCRUD):

    def __init__(
        self,
        session: AsyncSession,
        model: Order,
    ):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: Order = model

    async def update_order_status(
        self,
        order_id: UUID,
        new_status: OrderStatuses,
    ) -> Order | None:
        order: Order | None = await self.get_by_id(id=order_id)

        if not order:
            return None
        try:
            order.status = new_status
            await self.session.commit()
            await self.session.refresh(order)
            return order
        except IntegrityError as e:
            await self.session.rollback()
            return None

    async def get_orders_by_scroll(
        self,
        cursor: int | None,
        take: int | None,
        filters: OrderFilters,
    ) -> tuple[int | None, list]:
        order_filters = await self.prepare_filters(filters=filters)
        cursor = cursor if cursor is not None else 0
        stmt_count: Select = Select(func.count(self.model.id))
        stmt_count_using_filters = Select(func.count(self.model.id)).where(
            and_(*order_filters)
        )
        stmt: Select = Select(self.model).offset(cursor).where(and_(*order_filters))
        if take is not None:
            stmt = stmt.limit(take)

        result: Result = await self.session.execute(statement=stmt)
        result_count: Result = await self.session.execute(statement=stmt_count)
        result_count_using_filters: Result = await self.session.execute(
            statement=stmt_count_using_filters
        )
        count = result_count.scalar()
        count_filtered = result_count_using_filters.scalar()
        next_cursor = (
            cursor + take if take is not None and (cursor + take) <= count else None
        )

        return next_cursor, count_filtered, result.scalars().all()

    async def get_user_orders_by_scroll(
        self,
        user_id: UUID,
        cursor: int | None,
        take: int | None,
        filters: OrderFiltersCompressed,
    ) -> tuple[int | None, list]:
        order_filters = await self.prepare_filters(filters=filters)
        cursor = cursor if cursor is not None else 0
        stmt_count: Select = Select(func.count(self.model.id))
        stmt_count_using_filters = Select(func.count(self.model.id)).where(
            and_(
                *order_filters,
                self.model.user_id == user_id,
            )
        )
        stmt: Select = (
            Select(self.model)
            .offset(cursor)
            .where(
                and_(
                    *order_filters,
                    self.model.user_id == user_id,
                )
            )
        )
        if take is not None:
            stmt = stmt.limit(take)

        result: Result = await self.session.execute(statement=stmt)
        result_count: Result = await self.session.execute(statement=stmt_count)
        result_count_using_filters: Result = await self.session.execute(
            statement=stmt_count_using_filters
        )
        count = result_count.scalar()
        count_filtered = result_count_using_filters.scalar()
        next_cursor = (
            cursor + take if take is not None and (cursor + take) <= count else None
        )

        return next_cursor, count_filtered, result.scalars().all()

    async def prepare_filters(
        self,
        filters: OrderFilters | OrderFiltersCompressed,
    ) -> list:
        filters_list: list = []

        if hasattr(filters, "user_name") and filters.user_name:
            filters_list.append(self.model.user_name == filters.user_name)
        if hasattr(filters, "user_phone") and filters.user_phone:
            filters_list.append(self.model.user_phone == filters.user_phone)
        if hasattr(filters, "city_to_ship") and filters.city_to_ship:
            filters_list.append(self.model.city_to_ship == filters.city_to_ship)
        if hasattr(filters, "adress_to_ship") and filters.adress_to_ship:
            filters_list.append(self.model.adress_to_ship == filters.adress_to_ship)
        if hasattr(filters, "postal_code") and filters.postal_code:
            filters_list.append(self.model.postal_code == filters.postal_code)
        if filters.created_from:
            filters_list.append(self.model.created_at >= filters.created_from)
        if filters.created_to:
            filters_list.append(self.model.created_at <= filters.created_to)
        if filters.status:
            filters_list.append(self.model.status == filters.status)

        return filters_list
