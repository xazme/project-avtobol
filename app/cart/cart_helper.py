from .cart_model import Cart
from .cart_schema import CartResponseExtended


def convert_data_for_many_positions_in_cart(list_of_positions: list[Cart]):
    return [
        CartResponseExtended(
            user_id=order.user_id,
            product_id=order.product_id,
            product_brand=order.product.car_brand.name,
            product_series=order.product.car_series.name,
            product_part=order.product.car_part.name,
        )
        for order in list_of_positions
    ]
