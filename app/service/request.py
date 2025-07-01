from app.models.request import Request
from app.schema.request import RequestCreate, RequestUpdate
from app.service.base import Service


class RequestService(Service[Request, RequestCreate, RequestUpdate]):
    def __init__(self):
        super().__init__(Request)

requestService = RequestService()

__all__ = ["requestService"]