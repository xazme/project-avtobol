from enum import Enum


class CarType(str, Enum):
    PASSENGER_CAR = "легковой авто"
    TRUCK = "грузовой авто"
    SUV = "внедорожник"


class Season(str, Enum):
    WINTER = "зима"
    SUMMER = "лето"
