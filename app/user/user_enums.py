from enum import Enum


class UserRoles(str, Enum):
    ADMIN = "admin"
    OWNER = "owner"
    WORKER = "worker"
    SEO = "seo"
    CLIENT = "client"


class UserStatuses(str, Enum):
    ACTIVE = "active"
    BANNED = "banned"
