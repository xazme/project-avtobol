from typing import TYPE_CHECKING
from uuid import UUID
from fastapi import APIRouter, Query, Path, Body, Depends, status
from app.auth import requied_roles
from app.user import UserRoles
from app.cart import get_cart_handler
from app.core import settings
from .order_schema import OrderCreate, OrderResponse
from .order_dependencies import get_order_handler
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
    response_model=dict[str, str],
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    order_data: OrderCreate = Body(...),
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    cart_handler: "CartHandler" = Depends(get_cart_handler),
    order_handler: "OrderHandler" = Depends(get_order_handler),
) -> dict[str, str]:
    user_id = user.id
    user_positions = await cart_handler.get_all_user_positions(user_id=user_id)
    await order_handler.create_order(
        user_positions=user_positions,
        data=order_data,
    )
    await cart_handler.delete_all_positions(user_id=user_id)
    return {"message": "Order created successfully"}


@router.get(
    "/my-orders",
    summary="Get current user orders",
    description="Retrieve orders for the currently authenticated user",
    response_model=list[OrderResponse],
    status_code=status.HTTP_200_OK,
)
async def get_user_orders(
    status: OrderStatuses = Query(...),
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    order_handler: "OrderHandler" = Depends(get_order_handler),
) -> list[OrderResponse]:
    orders = await order_handler.get_all_orders_by_user_id(
        user_id=user.id,
        status=status,
    )
    return convert_data_for_order(list_of_orders=orders)


@router.get(
    "/user/{user_id}",
    summary="Get user orders (Worker access)",
    description="Retrieve orders for specific user (requires Worker role)",
    response_model=list[OrderResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(requied_roles([UserRoles.WORKER]))],
)
async def get_specific_user_orders(
    user_id: UUID = Path(...),
    status: OrderStatuses = Query(...),
    order_handler: "OrderHandler" = Depends(get_order_handler),
) -> list[OrderResponse]:
    orders = await order_handler.get_all_orders_by_user_id(
        user_id=user_id,
        status=status,
    )
    return convert_data_for_order(list_of_orders=orders)


@router.get(
    "/",
    summary="Get all orders (Worker access)",
    description="Retrieve paginated list of all orders (requires Worker role)",
    response_model=list[OrderResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(requied_roles([UserRoles.WORKER]))],
)
async def get_all_orders(
    status: OrderStatuses,
    page: int = 1,
    page_size: int = 10,
    order_handler: "OrderHandler" = Depends(get_order_handler),
) -> list[OrderResponse]:
    orders = await order_handler.get_all_orders(
        page=page,
        page_size=page_size,
        status=status,
    )
    return convert_data_for_order(list_of_orders=orders)


@router.patch(
    "/{order_id}/status",
    summary="Change order status",
    description="Update the status of an existing order",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
async def change_order_status(
    order_id: UUID = Path(...),
    status: OrderStatuses = Query(...),
    order_handler: "OrderHandler" = Depends(get_order_handler),
) -> OrderResponse:
    order = await order_handler.change_order_status(
        order_id=order_id,
        status=status,
    )
    return OrderResponse.model_validate(order)
