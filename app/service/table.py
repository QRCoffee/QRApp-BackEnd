from app.models.table import Table
from app.schema.table import TableCreate, TableUpdate
from app.service.base import Service


class TableService(Service[Table, TableCreate, TableUpdate]):
    def __init__(self):
        super().__init__(Table)

tableService = TableService()

__all__ = ["tableService"]