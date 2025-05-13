from typing import TYPE_CHECKING


def convert_data_for_car_brand_series_object(list_of_car_parts: list):
    data = [
        {
            "article": car_part.id,
            "brand_name": car_part.brand.name,
            "series_name": car_part.series.name,
            "part_type": car_part.car_part.name,
        }
        for car_part in list_of_car_parts
    ]

    return data
