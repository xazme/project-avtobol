from typing import TYPE_CHECKING
from uuid import UUID
from fastapi import APIRouter, Query, Path, Body, Depends, status
from app.auth import requied_roles
from app.user import UserRoles
from app.cart import get_cart_handler
from app.core import settings
from .order_schema import OrderCreate, OrderResponseExtended, OrderResponse
from .order_dependencies import get_order_handler, get_order_orchestrator
from .order_orchestrator import OrderOrchestrator
from .order_enums import OrderStatuses
from .order_helper import convert_data_for_order

if TYPE_CHECKING:
    from app.user import User
    from app.cart import CartHandler
    from .order_handler import OrderHandler

router = APIRouter(
    prefix=settings.api.order_prefix,
    tags=["Orders"],
)


@router.post(
    "/",
    summary="Create new order",
    description="Create a new order from current user's cart items",
    response_model=list[OrderResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    order_data: OrderCreate = Body(...),
    order_orchestrator: OrderOrchestrator = Depends(get_order_orchestrator),
) -> list[OrderResponse]:
    orders = await order_orchestrator.create_order(data=order_data)
    print(orders)
    return [OrderResponse.model_validate(order) for order in orders]


@router.get(
    "/my-orders",
    summary="Get current user orders",
    description="Retrieve orders for the currently authenticated user",
    response_model=list[OrderResponseExtended],
    status_code=status.HTTP_200_OK,
)
async def get_user_orders(
    status: OrderStatuses = Query(...),
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    order_handler: "OrderHandler" = Depends(get_order_handler),
) -> list[OrderResponseExtended]:
    orders = await order_handler.get_all_orders_by_user_id(
        user_id=user.id,
        status=status,
    )
    return convert_data_for_order(list_of_orders=orders)


@router.get(
    "/user/{user_id}",
    summary="Get user orders (Worker access)",
    description="Retrieve orders for specific user (requires Worker role)",
    response_model=list[OrderResponseExtended],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(requied_roles([UserRoles.WORKER]))],
)
async def get_specific_user_orders(
    user_id: UUID = Path(...),
    status: OrderStatuses = Body(...),
    order_handler: "OrderHandler" = Depends(get_order_handler),
) -> list[OrderResponseExtended]:
    orders = await order_handler.get_all_orders_by_user_id(
        user_id=user_id,
        status=status,
    )
    return convert_data_for_order(list_of_orders=orders)


@router.get(
    "/",
    summary="Get all orders (Worker access)",
    description="Retrieve paginated list of all orders (requires Worker role)",
    response_model=dict[str, int | None | list[OrderResponseExtended]],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(requied_roles([UserRoles.WORKER]))],
)
async def get_all_orders(
    search: str = Query(""),
    cursor: int | None = Query(None, gt=-1),
    take: int | None = Query(None, gt=0),
    status: OrderStatuses = Query(...),
    order_handler: "OrderHandler" = Depends(get_order_handler),
) -> dict[str, int | None | list[OrderResponseExtended]]:
    next_cursor, orders = await order_handler.get_all_orders_by_scroll(
        query=search,
        cursor=cursor,
        take=take,
        status=status,
    )
    return {
        "next_cursor": next_cursor if orders else None,
        "items": (convert_data_for_order(list_of_orders=orders)),
    }


@router.patch(
    "/{order_id}/status",
    summary="Change order status",
    description="Update the status of an existing order",
    response_model=OrderResponseExtended,
    status_code=status.HTTP_200_OK,
)
async def change_order_status(
    order_id: UUID = Path(...),
    status: OrderStatuses = Body(...),
    order_handler: "OrderHandler" = Depends(get_order_handler),
) -> OrderResponseExtended:
    order = await order_handler.change_order_status(
        order_id=order_id,
        status=status,
    )
    return OrderResponseExtended.model_validate(order)
