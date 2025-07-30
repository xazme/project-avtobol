from enum import Enum


class GearboxType(str, Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    ROBOTIC = "robotic"
    VARIATOR = "variator"


class FuelType(str, Enum):
    GASOLINE = "gasoline"
    DIESEL = "diesel"
    HYBRID = "hybrid"
    ELECTRIC = "electrick"
