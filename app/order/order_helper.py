from .order_model import Order
from .order_schema import OrderResponseExtended


def convert_data_for_order(list_of_orders: list[Order]) -> list[OrderResponseExtended]:
    return [
        OrderResponseExtended(
            id=order.id,
            user_id=order.user_id,
            article=order.product.article,
            user_name=order.user.name if order.user else order.user_name,
            user_phone=order.user.phone_number if order.user else order.user_phone,
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
