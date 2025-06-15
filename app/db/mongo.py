from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings
from app.models import Area, Permission, Restaurant, Table, User


class MongoDB:
    def __init__(
        self,
        url:str,
    ):
        self.client = AsyncIOMotorClient(url)
        self.database = AsyncIOMotorDatabase(
            client=self.client,
            name=settings.MONGO_DATABASE
        )

    async def initialize(self):
        await init_beanie(
            database=self.database,
            document_models=[
                User,
                Restaurant,
                Area,
                Table,
                Permission,
            ]
        )
        return self


Mongo = MongoDB(settings.MONGO_URL)