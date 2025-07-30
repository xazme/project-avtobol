from enum import Enum


class CarType(str, Enum):
    PASSENGER_CAR = "passenger car"
    TRUCK = "truck"
    SUV = "suv"


class Season(str, Enum):
    WINTER = "winter"
    SUMMER = "summer"
