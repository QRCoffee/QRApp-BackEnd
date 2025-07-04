from app.models.branch import Branch
from app.schema.branch import BranchCreate, BranchUpdate
from app.service.base import Service


class BranchService(Service[Branch, BranchCreate, BranchUpdate]):
    def __init__(self):
        super().__init__(Branch)


branchService = BranchService()

__all__ = ["branchService"]
