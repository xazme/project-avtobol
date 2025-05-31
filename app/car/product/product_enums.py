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
    ELECTRIC = "electric"


class BodyType(str, Enum):
    SEDAN = "sedan"
    HATCHBACK = "hatchback"
    COUPE = "coupe"
    UNIVERSAL = "universal"
    MINIVAN = "minivan"
    JEEP = "jeep"
    MINIBUS = "minibus"
    CONVERTIBLE = "convertible"
    VAN = "van"
    LIFTBACK = "liftback"
    COMPACT = "compact"
    TRACTOR = "tractor"


class ProductCondition(str, Enum):
    NEW = "new"
    USED = "used"
