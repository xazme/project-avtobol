from enum import Enum


class OrderStatuses(str, Enum):
    OPEN = "open"  # заказ создан, ждёт обработки
    PROCESSING = "processing"  # идёт обработка: сборка, проверка
    WAITING_FOR_SHIP = "waiting_for_shipment"  # собран, ждёт отправки
    SHIPPED = "shipped"  # передан в доставку
    DELIVERED = "delivered"  # получен клиентом
    RETURNED = "returned"  # клиент вернул товар
    CANCELLED = "cancelled"  # заказ отменён (по инициативе клиента/системы)
    DENIED = "denied"  # отклонён (например, товар недоступен)
    ON_HOLD = "on_hold"  # временная приостановка (нет на складе, блокировка)
    CLOSE = "closed"  # заказ закрыт (успешно завершён или архивирован)
