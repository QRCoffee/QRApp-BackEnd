from app.models.group import Group
from app.schema.group import GroupCreate, GroupUpdate
from app.service.base import Service


class GroupService(Service[Group, GroupCreate, GroupUpdate]):
    def __init__(self):
        super().__init__(Group)
        
groupService = GroupService()

__all__ = ["groupService"]