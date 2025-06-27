from enum import Enum


class GearboxType(str, Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    ROBOTIC = "robotic"
    VARIATOR = "CVT"


class FuelType(str, Enum):
    GASOLINE = "gasoline"
    DIESEL = "diesel"
    HYBRID = "hybrid"
    ELECTRIC = "electricity"


class BodyType(str, Enum):
    SEDAN = "sedan"
    HATCHBACK = "hatchback"
    COUPE = "coupe"
    UNIVERSAL = "wagon"
    MINIVAN = "minivan"
    JEEP = "SUV"
    MINIBUS = "minibus"
    CONVERTIBLE = "convertible"
    VAN = "van"
    LIFTBACK = "liftback"
    COMPACT = "compact"
    TRACTOR = "tractor"


class ProductCondition(str, Enum):
    NEW = "new"
    USED = "used"


class Availability(str, Enum):
    IN_STOCK = "in stock"
    CUSTOM = "custom order"


class Currency(str, Enum):
    PL = "ZLOTY"
    USD = "USD"
