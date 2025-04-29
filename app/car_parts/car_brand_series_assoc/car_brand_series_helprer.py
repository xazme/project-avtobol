from typing import TYPE_CHECKING


def convert_data_for_car_brand_series_object(list_of_car_parts: list):
    data = []
    for car_part in list_of_car_parts:
        bebe = {
            "article": car_part.id,
            "brand name": car_part.brand.name,
            "series name": car_part.series.name,
            "part type": car_part.car_part.name,
        }
        data.append(bebe)
    return data


def convert_data_for_car_brand_series_object(list_of_car_parts: list):
    data = [
        {
            "article": car_part.id,
            "brand name": car_part.brand.name,
            "series name": car_part.series.name,
            "part type": car_part.car_part.name,
        }
        for car_part in list_of_car_parts
    ]

    return data
