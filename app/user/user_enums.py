from enum import Enum


class UserRoles(str, Enum):
    ADMIN = "admin"
    WORKER = "worker"
    CLIENT = "client"


class UserStatuses(str, Enum):
    ACTIVE = "active"
    BANNED = "banned"
