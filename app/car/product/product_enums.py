from enum import Enum


class GearboxType(str, Enum):
    MANUAL = "механическая"
    AUTOMATIC = "автомат"
    ROBOTIC = "робот"
    VARIATOR = "вариатор"


class FuelType(str, Enum):
    GASOLINE = "бензин"
    DIESEL = "дизель"
    HYBRID = "гибрид"
    ELECTRIC = "электричество"


class BodyType(str, Enum):
    SEDAN = "седан"
    HATCHBACK = "хэтчбек"
    COUPE = "купе"
    UNIVERSAL = "универсал"
    MINIVAN = "минивэн"
    JEEP = "джип"
    MINIBUS = "микроавтобус"
    CONVERTIBLE = "кабриолет"
    VAN = "фурго"
    LIFTBACK = "лифтбэк"
    COMPACT = "компактный"
    TRACTOR = "трактор"


class ProductCondition(str, Enum):
    NEW = "новое"
    USED = "Б/У"


class Currency(str, Enum):
    PL = "ZLOTY"
    USD = "USD"
