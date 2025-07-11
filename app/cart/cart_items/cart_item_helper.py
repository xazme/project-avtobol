from .cart_item_model import CartItem
from .cart_item_schema import CartItemResponseExtended


def convert_cart_items(cart_items: list[CartItem]):

    items = []

    for item in cart_items:
        product_id = item.product.id
        product_article = item.product.article
        car_brand = item.product.car_brand.name
        car_series = item.product.car_series.name
        car_part_type = item.product.car_part.name
        price = item.product.price
        discount = item.product.discount

        cart_item = CartItemResponseExtended(
            id=item.id,
            product_id=product_id,
            article=product_article,
            car_brand_name=car_brand,
            car_series_name=car_series,
            car_part_type=car_part_type,
            price=price,
            discount=discount,
        )

        items.append(cart_item)

    return items
