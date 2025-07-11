from app.car.product.product_schema import ProductResponseCompressed
from .order_model import Order
from .order_schema import OrderResponse, OrderResponseExtend
from ..order_item import OrderItem


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


def convert_order_data_for_items(
    list_of_order_items: list[OrderItem],
):
    list_of_converted_items = []
    for order_item in list_of_order_items:
        product_data = {
            "id": order_item.product.id,
            "article": order_item.product.article,
            "car_brand_name": order_item.product.car_brand.name,
            "car_series_name": order_item.product.car_series.name,
            "car_part_name": order_item.product.car_part.name,
            "price": order_item.product.price,
            "discount": order_item.product.discount,
            "picture": order_item.product.pictures[0],
        }
        data = ProductResponseCompressed.model_validate(product_data)
        list_of_converted_items.append(data)

    return OrderResponseExtend(
        products=list_of_converted_items,
        products_count=len(list_of_converted_items),
    )
