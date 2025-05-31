from .product_model import Product
from .product_schema import ProductResponse


def convert_data_for_list_of_products(
    list_of_car_parts: list[Product],
) -> list[ProductResponse]:
    data = []
    for car_part in list_of_car_parts:
        response = ProductResponse(
            id=car_part.id,
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
        )
        data.append(response)

    return data


def convert_data_for_product(
    car_part: Product,
) -> ProductResponse:
    response = ProductResponse(
        id=car_part.id,
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
    )
    return response
