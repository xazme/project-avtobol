from enum import Enum


class Season(str, Enum):
    WINTER = "winter"
    SUMMER = "summer"
    ALL_SEASON = "any"


class CarType(str, Enum):
    PASSENGER = "passenger"
    TRUCK = "truck"
    SUV = "suv"
