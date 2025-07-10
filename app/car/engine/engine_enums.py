from enum import Enum


class GearboxType(str, Enum):
    MANUAL = "механическая"
    AUTOMATIC = "автоматическая"
    ROBOTIC = "робот"
    VARIATOR = "вариатор"


class FuelType(str, Enum):
    GASOLINE = "бензин"
    DIESEL = "дизель"
    HYBRID = "гибрид"
    ELECTRIC = "электрическая"
