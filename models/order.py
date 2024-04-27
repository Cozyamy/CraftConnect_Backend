from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    DECLINED = "DECLINED"

    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
