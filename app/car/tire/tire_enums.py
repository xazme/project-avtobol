from enum import Enum


class Season(str, Enum):
    WINTER = "зима"
    SUMMER = "лето"
    ALL_SEASON = "всесезонный"


class CarType(str, Enum):
    PASSENGER = "легковой"
    TRUCK = "грузовой"
    SUV = "внедорожник"
