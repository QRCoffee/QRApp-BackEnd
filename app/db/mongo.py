from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings
from app.models import User


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
            document_models=[User]
        )
        return self


Mongo = MongoDB(f"mongodb+srv://nhathuyd4hp:admin.nhathuyd4hp@qrapp.p6y4b66.mongodb.net/{settings.MONGO_DATABASE}?retryWrites=true&w=majority")