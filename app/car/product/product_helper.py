from .product_model import Product
from .product_schema import ProductResponseExtend


def convert_data(
    product_data: Product | list[Product],
    is_private: bool = False,
) -> ProductResponseExtend | list[ProductResponseExtend]:

    def _convert(car_part: Product) -> ProductResponseExtend:
        data = {
            "id": car_part.id,
            "OEM": car_part.OEM,
            "VIN": car_part.VIN,
            "pictures": car_part.pictures,
            "car_brand_name": car_part.car_brand.name,
            "car_series_name": car_part.car_series.name,
            "car_part_name": car_part.car_part.name,
            "year": car_part.year,
            "volume": car_part.volume,
            "gearbox": car_part.gearbox,
            "fuel": car_part.fuel,
            "type_of_body": car_part.type_of_body,
            "condition": car_part.condition,
            "description": car_part.description,
            "price": car_part.price,
            "discount": car_part.discount,
            "currency": car_part.currency,
            "availability": car_part.availability,
            "count": car_part.count,
            # Диски
            "disc_diametr": car_part.disc_diametr,
            "disc_width": car_part.disc_width,
            "disc_ejection": car_part.disc_ejection,
            "disc_dia": car_part.disc_dia,
            "disc_holes": car_part.disc_holes,
            "disc_pcd": car_part.disc_pcd,
            "disc_brand_name": (
                car_part.disc_brand.name if car_part.disc_brand else None
            ),
            "disc_model": car_part.disc_model,
            # Шины
            "tires_diametr": car_part.tires_diametr,
            "tires_width": car_part.tires_width,
            "tires_height": car_part.tires_height,
            "tires_index": car_part.tires_index,
            "tires_car_type": car_part.tires_car_type,
            "tires_brand_name": (
                car_part.tire_brand.name if car_part.tire_brand else None
            ),
            "tires_model": car_part.tires_model,
            "tires_season": car_part.tires_season,
            "tires_residue": car_part.tires_residue,
        }

        if is_private:
            data.update(
                {
                    "note": car_part.note,
                    "is_available": car_part.is_available,
                    "is_printed": car_part.is_printed,
                    "created_at": car_part.created_at,
                    "post_by": car_part.post_by,
                }
            )

        return ProductResponseExtend(**data)

    if isinstance(product_data, list):
        return [_convert(car_part) for car_part in product_data]
    return _convert(product_data)
