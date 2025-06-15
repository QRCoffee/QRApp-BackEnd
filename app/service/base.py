from typing import Any, Generic, List, Optional, Type, TypeVar, Union

from beanie import Document
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Document)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class Service(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def find_one_by(self, by: str = "_id", value: Any = None) -> Optional[ModelType]:
        if by == "_id":
            return await self.model.get(value,fetch_links=True)
        return await self.model.find_one({by: value},fetch_links=True)

    async def find_many_by(
        self,
        conditions: dict[str,Any] | None = None,
        skip: int | None = None,
        limit: int | None = None,
    ) -> List[ModelType]:
        users = await self.model.find_many(
            conditions,
            skip= skip,
            limit = limit,
            fetch_links=True,
        ).to_list()
        return users

    async def create(self, data: Union[dict, CreateSchemaType]) -> ModelType:
        if isinstance(data, BaseModel):
            data = data.model_dump()
        doc = self.model(**data)
        await doc.insert()
        return doc

    async def update(self, id: Any, data: Union[dict, UpdateSchemaType]) -> Optional[ModelType]:
        db_item = await self.model.get(id)
        if not db_item:
            return None

        if isinstance(data, BaseModel):
            data = data.model_dump(exclude_unset=True)

        for key, value in data.items():
            setattr(db_item, key, value)

        await db_item.save()
        return db_item

    async def delete(self, id: Any) -> bool:
        db_item = await self.model.get(id)
        if not db_item:
            return False

        await db_item.delete()
        return True
