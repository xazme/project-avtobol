from .product_model import Product
from .product_schema import (
    ProductResponse,
    ProductResponsePublic,
    ProductResponsePrivate,
)
from ..tire.tire import TireResponse
from ..disc.disc import DiscResponse
from ..engine import EngineResponse


def _get_details(
    product: Product,
) -> TireResponse | DiscResponse | EngineResponse | None:
    if product.tire:
        return TireResponse.model_validate(product.tire)
    if product.disc:
        return DiscResponse.model_validate(product.disc)
    if product.engine:
        return EngineResponse.model_validate(product.engine)
    return None


def convert_product_data_public(
    product_data: Product | list[Product],
) -> ProductResponsePublic | list[ProductResponsePublic]:
    def _convert(product: Product) -> ProductResponsePublic:
        data = {
            "id": product.id,
            "article": product.article,
            "OEM": product.OEM,
            "VIN": product.VIN,
            "pictures": product.pictures,
            "car_series_year": product.car_series.year,
            "car_part_name": product.car_part.name,
            "car_part_name_latin": product.car_part.latin_name,
            "car_brand_name": product.car_brand.name,
            "car_series_name": product.car_series.name,
            "year": product.year,
            "details": _get_details(product),
            "description": product.description,
            "price": product.price,
            "discount": product.discount,
            "currency": product.currency,
            "count": product.count,
            "availability": product.availability,
        }
        return ProductResponsePublic(**data)

    if isinstance(product_data, list):
        return [_convert(product) for product in product_data]
    return _convert(product_data)


def convert_product_data_private(
    product_data: Product | list[Product],
) -> ProductResponsePrivate | list[ProductResponsePrivate]:
    def _convert(product: Product) -> ProductResponsePrivate:
        data = {
            "id": product.id,
            "article": product.article,
            "OEM": product.OEM,
            "VIN": product.VIN,
            "pictures": product.pictures,
            "car_series_year": product.car_series.year,
            "car_part_name": product.car_part.name,
            "car_brand_id": product.car_brand_id,
            "car_brand_name": product.car_brand.name,
            "car_series_id": product.car_series_id,
            "car_series_name": product.car_series.name,
            "note": product.note,
            "car_part_id": product.car_part_id,
            "idriver_id": product.idriver_id,
            "allegro_id": product.allegro_id,
            "is_printed": product.is_printed,
            "is_available": product.is_available,
            "created_at": product.created_at,
            "post_by": product.post_by,
            "year": product.year,
            "details": _get_details(product),
            "description": product.description,
            "price": product.price,
            "discount": product.discount,
            "currency": product.currency,
            "count": product.count,
            "availability": product.availability,
        }
        return ProductResponsePrivate(**data)

    if isinstance(product_data, list):
        return [_convert(product) for product in product_data]
    return _convert(product_data)


def convert_product_data_basic(
    product_data: Product | list[Product],
) -> ProductResponse:

    def _convert(product: Product) -> ProductResponse:
        data = {
            "id": product.id,
            "article": product.article,
            "OEM": product.OEM,
            "VIN": product.VIN,
            "car_brand_id": product.car_brand_id,
            "car_series_id": product.car_series_id,
            "car_part_id": product.car_part_id,
            "year": product.year,
            "type_of_body": product.type_of_body,
            "description": product.description,
            "price": product.price,
            "discount": product.discount,
            "currency": product.currency,
            "condition": product.condition,
            "availability": product.availability,
            "note": product.note,
            "count": product.count,
            "pictures": product.pictures,
            "is_printed": product.is_printed,
            "is_available": product.is_available,
            "created_at": product.created_at,
            "idriver_id": product.idriver_id,
            "allegro_id": product.allegro_id,
        }
        return ProductResponse(**data)

    if isinstance(product_data, list):
        return [_convert(product) for product in product_data]
    return _convert(product_data)
