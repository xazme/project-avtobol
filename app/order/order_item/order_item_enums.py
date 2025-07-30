from enum import Enum


class OrderItemStatus(str, Enum):
    PENDING = "pending"  # заказ в процессе — товар ещё занят
    PREPARING = "preparing"  # сборка — занят
    SHIPPED = "shipped"  # отправлен — занят
    DELIVERED = "delivered"  # доставлен — занят

    # Статусы, при которых товар можно вернуть в поток:
    CANCELLED = "cancelled"  # товар отменён — можно снова продавать
    OUT_OF_STOCK = "out_of_stock"  # технически занят, но можно освободить
    RETURNED = "returned"  # вернулся — снова доступен
    REFUNDED = "refunded"  # деньги вернули — товар больше не привязан
    DENIED = "denied"  # (если добавишь) — товар не прошёл проверку
