from .order_model import Order
from .order_schema import OrderResponseExtended


def convert_data_for_order(list_of_orders: list[Order]):
    return [
        OrderResponseExtended(
            id=order.id,
            user_id=order.user_id,
            user_name=order.user.name,
            user_phone=order.user.phone_number,
            product_id=order.product_id,
            product_article=order.product.article,
            product_brand=order.product.car_brand.name,
            product_series=order.product.car_series.name,
            product_part=order.product.car_part.name,
            created_at=order.created_at,
            description=order.description,
            status=order.status,
        )
        for order in list_of_orders
    ]
