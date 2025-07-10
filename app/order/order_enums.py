from enum import Enum


class OrderStatuses(str, Enum):
    OPEN = "open"
    CLOSE = "close"
