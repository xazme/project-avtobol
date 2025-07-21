from typing import TYPE_CHECKING
from uuid import UUID
from fastapi import APIRouter, Body, Path, Query, Depends, status
from app.core import settings
from app.user.user_enums import UserRoles
from app.auth.auth_guard import required_roles
from .order_schema import (
    OrderCreate,
    OrderResponse,
    OrderManualResponse,
    OrderItemResponse,
    OrderFilters,
    OrderFiltersCompressed,
    OrderUpdate,
)
from .order_enums import OrderStatuses
from .order_dependencies import get_order_orchestrator
from .order_helper import convert_order_data_for_items

router = APIRouter(
    prefix=settings.api.order_prefix,
    tags=["Orders"],
)

if TYPE_CHECKING:
    from app.user import User
    from .order_orchestrator import OrderOrchestrator


@router.post(
    "/create-order",
    summary="Create order",
    description="Create a new order from user's cart",
    status_code=status.HTTP_201_CREATED,
    response_model=OrderResponse,
)
async def create_order(
    order_data: OrderCreate = Body(...),
    user: "User" = Depends(required_roles(allowed_roles=[UserRoles.CLIENT])),
    order_orchestrator: "OrderOrchestrator" = Depends(get_order_orchestrator),
):
    order, denied = await order_orchestrator.create_order(
        user_id=user.id,
        data=order_data,
    )
    return OrderResponse.model_validate(order)


@router.post(
    "/private",
    summary="Create order. Worker Access",
    description="Create a new order from user's cart",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(required_roles(allowed_roles=[UserRoles.WORKER]))],
    response_model=OrderManualResponse,
)
async def create_order_manually(
    order_data: OrderCreate = Body(...),
    product_ids: list[str] = Body(...),
    order_orchestrator: "OrderOrchestrator" = Depends(get_order_orchestrator),
) -> OrderManualResponse:
    order, denied_articles = await order_orchestrator.create_order_manually(
        data=order_data,
        product_ids=product_ids,
    )
    return OrderManualResponse(denied=denied_articles, order_data=order)


@router.get(
    "/all",
    summary="Get all orders.",
    description="Retrieve all orders.",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(required_roles(allowed_roles=[UserRoles.WORKER]))],
    response_model=dict[str, int | None | list[OrderResponse]],
)
async def get_all_orders(
    cursor: int | None = Query(None, gt=-1),
    take: int | None = Query(None, gt=0),
    filters: OrderFilters = Depends(),
    order_orchestrator: "OrderOrchestrator" = Depends(get_order_orchestrator),
) -> dict[str, int | None | list[OrderResponse]]:
    next_cursor, total_count, orders = (
        await order_orchestrator.order_handler.get_all_orders(
            cursor=cursor,
            take=take,
            filters=filters,
        )
    )
    return {
        "next_cursor": next_cursor,
        "total_count": total_count,
        "items": [OrderResponse.model_validate(order) for order in orders],
    }


@router.get(
    "/my-orders",
    summary="Get user orders",
    description="Retrieve all user orders.",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, int | None | list[OrderResponse]],
)
async def get_user_orders(
    cursor: int | None = Query(None, gt=-1),
    take: int | None = Query(None, gt=0),
    filters: OrderFiltersCompressed = Depends(),
    user: "User" = Depends(required_roles(allowed_roles=[UserRoles.CLIENT])),
    order_orchestrator: "OrderOrchestrator" = Depends(get_order_orchestrator),
) -> dict[str, int | None | list[OrderResponse]]:
    next_cursor, total_count, orders = (
        await order_orchestrator.order_handler.get_user_orders(
            user_id=user.id,
            cursor=cursor,
            take=take,
            filters=filters,
        )
    )
    return {
        "next_cursor": next_cursor,
        "total_count": total_count,
        "items": [OrderResponse.model_validate(order) for order in orders],
    }


@router.get(
    "/{order_id}",
    summary="Get order details.",
    description="Retrieve detailed information about a specific order",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(required_roles([UserRoles.WORKER, UserRoles.CLIENT]))],
    response_model=OrderItemResponse,
)
async def get_order_items(
    order_id: UUID = Path(...),
    order_orchestrator: "OrderOrchestrator" = Depends(get_order_orchestrator),
) -> OrderItemResponse:
    order_items = (
        await order_orchestrator.order_item_handler.get_order_items_by_order_id(
            order_id=order_id
        )
    )
    return convert_order_data_for_items(list_of_order_items=order_items)


@router.put(
    "/update/{order_id}",
    summary="Update order",
    description="Update order information (only for client)",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(required_roles([UserRoles.WORKER]))],
    response_model=OrderResponse,
)
async def update_order(
    order_id: UUID = Path(...),
    update_data: OrderUpdate = Body(...),
    order_orchestrator: "OrderOrchestrator" = Depends(get_order_orchestrator),
):
    updated_order = await order_orchestrator.order_handler.update_order(
        order_id=order_id,
        data=update_data,
    )
    return OrderResponse.model_validate(updated_order)


@router.patch(
    "/order/{order_id}/status",
    summary="Update order status",
    description="Update order status (only for admin/manager)",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(required_roles([UserRoles.WORKER]))],
    response_model=OrderResponse,
)
async def update_order_status(
    order_id: UUID = Path(...),
    new_status: OrderStatuses = Body(...),
    order_orchestrator: "OrderOrchestrator" = Depends(get_order_orchestrator),
):
    updated_order = await order_orchestrator.order_handler.update_order_status(
        order_id=order_id,
        new_status=new_status,
    )
    return OrderResponse.model_validate(updated_order)


@router.patch(
    "/order_item/{order_item_id}/status",
    summary="Update order item status",
    description="Update order status (only for admin/manager)",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(required_roles([UserRoles.WORKER]))],
    response_model=OrderResponse,
)
async def update_order_item_status(
    order_item_id: UUID = Path(...),
    new_status: OrderStatuses = Body(...),
    order_orchestrator: "OrderOrchestrator" = Depends(get_order_orchestrator),
):
    updated_order = await order_orchestrator.update_order_item_status(
        order_item_id=order_item_id,
        new_status=new_status,
    )
    return OrderResponse.model_validate(updated_order)
