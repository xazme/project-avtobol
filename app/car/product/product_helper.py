from typing import TYPE_CHECKING


def convert_data_for_product(list_of_car_parts: list):
    data = [
        {
            "article": car_part.id,
            "brand_name": car_part.car_brand.name,
            "series_name": car_part.car_series.name,
            "part_type": car_part.car_part.name,
            "pictures": car_part.pictures,
        }
        for car_part in list_of_car_parts
    ]

    return data
