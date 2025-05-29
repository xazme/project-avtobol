from typing import TYPE_CHECKING
from uuid import UUID
from fastapi import APIRouter, Depends
from app.auth import requied_roles
from app.user import UserRoles
from app.cart import get_cart_handler
from .order_schema import OrderCreate, OrderResponse
from .order_dependencies import get_order_handler
from .order_enums import OrderStatuses
from .order_helper import convert_data_for_order

if TYPE_CHECKING:
    from app.user import User
    from app.cart import CartHandler
    from .order_handler import OrderHandler

router = APIRouter(prefix="/orders", tags=["suka"])


@router.post(
    "/ebe",
    response_model=dict,
)
async def create_order(
    order_data: OrderCreate,
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    cart_hander: "CartHandler" = Depends(get_cart_handler),
    order_handler: "OrderHandler" = Depends(get_order_handler),
):
    user_id = user.id
    user_positions = await cart_hander.get_all_user_positions(user_id=user_id)
    await order_handler.create_order(
        user_positions=user_positions,
        data=order_data,
    )
    await cart_hander.delete_all_positions(user_id=user_id)
    return {"msg": "SUCCESS"}


@router.get("/my-orders")
async def get_user_orders(
    status: OrderStatuses,
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    order_handler: "OrderHandler" = Depends(get_order_handler),
):
    orders = await order_handler.get_all_orders_by_user_id(
        user_id=user.id,
        status=status,
    )
    return convert_data_for_order(list_of_orders=orders)


@router.get(
    "/all-user-orders",
    dependencies=[
        Depends(requied_roles([UserRoles.WORKER])),
    ],
)
async def get_user_orders(
    user_id: UUID,
    status: OrderStatuses,
    order_handler: "OrderHandler" = Depends(get_order_handler),
):
    orders = await order_handler.get_all_orders_by_user_id(
        user_id=user_id,
        status=status,
    )
    return convert_data_for_order(list_of_orders=orders)


@router.get(
    "/all-user-orders-worker",
    dependencies=[
        Depends(requied_roles([UserRoles.WORKER])),
    ],
)
async def get_user_orders(
    status: OrderStatuses,
    page: int,
    page_size: int,
    order_handler: "OrderHandler" = Depends(get_order_handler),
):
    orders = await order_handler.get_all_orders(
        page=page,
        page_size=page_size,
        status=status,
    )
    return convert_data_for_order(list_of_orders=orders)


@router.put("/switch-status")
async def change_order_status(
    status: OrderStatuses,
    order_id: UUID,
    order_handler: "OrderHandler" = Depends(get_order_handler),
):
    order = await order_handler.change_order_status(order_id=order_id, status=status)
    return OrderResponse.model_validate(order)
