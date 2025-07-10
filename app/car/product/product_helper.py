from .product_model import Product
from .product_schema import ProductResponseExtend
from ..tire.tire import TireResponse
from ..disc.disc import DiscResponse
from ..engine import EngineResponse


def convert_data(
    product_data: Product | list[Product],
    is_private: bool = False,
) -> ProductResponseExtend | list[ProductResponseExtend]:
    def _convert(product: Product) -> ProductResponseExtend:
        data = {
            "id": product.id,
            "article": product.article,
            "OEM": product.OEM,
            "VIN": product.VIN,
            "pictures": product.pictures,
            "car_brand_id": product.car_brand_id if is_private else None,
            "car_brand_name": product.car_brand.name,
            "car_series_id": product.car_series_id if is_private else None,
            "car_series_name": product.car_series.name,
            "car_part_id": product.car_part_id if is_private else None,
            "car_part_name": product.car_part.name,
            "year": product.year,
            "type_of_body": product.type_of_body,
            "condition": product.condition,
            "description": product.description,
            "price": product.price,
            "discount": product.discount,
            "currency": product.currency,
            "availability": product.availability,
            "count": product.count,
            "engine": (
                EngineResponse.model_validate(product.engine)
                if product.engine
                else None
            ),
            "disc": DiscResponse.model_validate(product.disc) if product.disc else None,
            "tire": TireResponse.model_validate(product.tire) if product.tire else None,
        }

        if is_private:
            data.update(
                {
                    "note": product.note,
                    "is_available": product.is_available,
                    "is_printed": product.is_printed,
                    "created_at": product.created_at,
                    "post_by": product.post_by,
                }
            )

        return ProductResponseExtend(**data)

    if isinstance(product_data, list):
        return [_convert(prod) for prod in product_data]
    return _convert(product_data)
