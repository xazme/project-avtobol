from .cart_model import Cart


def convert_data_for_cart(list_of_orders: list[Cart]):
    {
        {
            "user_id": order.user_id,
            "product_id": order.product_id,
            "product_car_brand": order.product.car_brand.name,
            "product_car_series": order.product.car_series.name,
            "product_car_part": order.product.car_part.name,
        }
        for order in list_of_orders
    }
