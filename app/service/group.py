from app.models.group import Group
from app.schema.group import GroupCreate, GroupUpdate
from app.service.base import Service
from beanie import PydanticObjectId

class GroupService(Service[Group, GroupCreate, GroupUpdate]):
    def __init__(self):
        super().__init__(Group)
    async def find_by_business(self,business:PydanticObjectId):
        """ Tìm group trong doanh nghiệp
        Args:
            business (PydanticObjectId): ID Doanh nghiệp
        """
        return await self.model.find_many(
            {"scope._id": business},  
            fetch_links=True
        ).to_list()
groupService = GroupService()

__all__ = ["groupService"]