from enum import Enum


class Statuses(str, Enum):
    ONLIME = "online"
    OFFLINE = "offline"
    BANNED = "banned"


class Roles(str, Enum):
    OWNER = "owner"
    WORKER = "worker"
    SEO = "seo"


class Tokens(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
