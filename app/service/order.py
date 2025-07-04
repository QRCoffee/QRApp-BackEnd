from app.models.order import Order
from app.schema.order import OrderCreate, OrderUpdate
from app.service.base import Service


class OrderService(Service[Order, OrderCreate, OrderUpdate]):
    def __init__(self):
        super().__init__(Order)

orderService = OrderService()

__all__ = ["orderService"]