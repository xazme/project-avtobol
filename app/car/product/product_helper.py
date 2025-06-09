from .product_model import Product
from .product_schema import ProductResponse


def convert_data(
    product_data: Product | list[Product],
) -> ProductResponse | list[ProductResponse]:
    def _convert(car_part: Product) -> ProductResponse:
        return ProductResponse(
            id=car_part.id,
            OEM=car_part.OEM,
            VIN=car_part.VIN,
            note=car_part.note,
            pictures=car_part.pictures,
            car_brand_name=car_part.car_brand.name,
            car_series_name=car_part.car_series.name,
            car_part_name=car_part.car_part.name,
            year=car_part.year,
            volume=car_part.volume,
            gearbox=car_part.gearbox,
            fuel=car_part.fuel,
            type_of_body=car_part.type_of_body,
            condition=car_part.condition,
            description=car_part.description,
            real_price=car_part.real_price,
            fake_price=car_part.fake_price,
            count=car_part.count,
            is_available=car_part.is_available,
            is_printed=car_part.is_printed,
            created_at=car_part.created_at,
        )

    if isinstance(product_data, list):
        return [_convert(car_part) for car_part in product_data]
    return _convert(product_data)
