from enum import Enum


class Statuses(str, Enum):
    ACTIVE = "active"
    BANNED = "banned"


class OrderStatuses(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    DENIED = "denied"


class Roles(str, Enum):
    OWNER = "owner"
    WORKER = "worker"
    SEO = "seo"
    CLIENT = "client"


class Tokens(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
