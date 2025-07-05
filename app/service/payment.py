from app.models.payment import Payment
from app.schema.payment import PaymentCreate, PaymentUpdate
from app.service.base import Service


class PaymentService(Service[Payment, PaymentCreate, PaymentUpdate]):
    def __init__(self):
        super().__init__(Payment)


paymentService = PaymentService()

__all__ = ["paymentService"]
