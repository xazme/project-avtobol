from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_name: str
    user_phone: str
    description: str
    city_to_ship: str
    adress_to_ship: str
    postal_code: str
