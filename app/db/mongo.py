from beanie import init_beanie,Document
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import List
from app.core.config import settings
from app.models import Permission,User,Business,BusinessType,Group,Branch
from app.service import permissionService,userService
from app.schema.user import Administrator
from app.schema.permission import PermissionCreate
class MongoDB:
    def __init__(
        self,
        url:str,
        database: str,
        documents:List[Document],
    ):
        self.client = AsyncIOMotorClient(url)
        self.database = AsyncIOMotorDatabase(
            client=self.client,
            name=database,
        )
        self.documents = documents

    async def initialize(self):
        await init_beanie(
            database=self.database,
            document_models=self.documents
        )
        for document in self.documents:
            for action in document.get_actions():
                if await permissionService.find_one_by(
                    by = "code",
                    value = f"{action.lower()}.{document.__name__.lower()}",
                ) is None:
                    await permissionService.create(PermissionCreate(
                        code = f"{action.lower()}.{document.__name__.lower()}",
                        description=f"{action.upper()} {document.__name__.upper()}"
                    ))
        if not await userService.find_one_by(
            by = "username",
            value = "admin"
        ):
            await userService.create(Administrator(
                username = settings.ADMIN_USERNAME,
                password = settings.ADMIN_PASSWORD,
                name = "Administrator",
                phone = "Administrator",
                address = "Administrator",
            ))
        return self


Mongo = MongoDB(
    url = settings.MONGO_URL,
    database= settings.MONGO_DATABASE,
    documents=[
        User,
        Permission,
        Group,
        BusinessType,
        Business,
        Branch,
    ]
)