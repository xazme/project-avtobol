from .order_model import Order
from .order_schema import OrderResponse


def convert_order_data(order: Order) -> OrderResponse:
    order_data = {
        "id": order.id,
        "user_id": order.user_id,
        "user_name": order.user_name,
        "user_phone": order.user_phone,
        "description": order.description,
        "city_to_ship": order.city_to_ship,
        "adress_to_ship": order.adress_to_ship,
        "postal_code": order.postal_code,
        "status": order.status,
        "created_at": order.created_at,
    }

    return OrderResponse.model_validate(order_data)
