from typing import Any, Generic, List, Optional, Type, TypeVar, Union,Dict

from beanie import Document
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Document)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class Service(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    # 1. Tìm theo ID
    async def find(self, id: Any) -> Optional[ModelType]:
        return await self.model.get(id)

    # 2. Tìm một document theo điều kiện
    async def find_one(self, conditions: Dict[str, Any] | None = None) -> Optional[ModelType]:
        conditions = conditions or {}
        return await self.model.find_one(conditions)

    # 3. Tìm nhiều document theo điều kiện
    async def find_many(
        self,
        conditions: Dict[str, Any] | None = None,
        skip: int | None = None,
        limit: int | None = None,
    ) -> List[ModelType]:
        conditions = conditions or {}
        return await self.model.find_many(
            conditions,
            skip=skip,
            limit=limit,
        ).to_list()

    # 4. Ghi 1 document
    async def insert(self, data: Union[dict, CreateSchemaType]) -> ModelType:
        if isinstance(data, BaseModel):
            data = data.model_dump()
        doc = self.model(**data)
        await doc.insert()
        return doc

    # 5. Ghi nhiều document
    async def insert_many(self, data_list: List[Union[dict, CreateSchemaType]]) -> List[ModelType]:
        docs = []
        for data in data_list:
            if isinstance(data, BaseModel):
                data = data.model_dump()
            docs.append(self.model(**data))
        return await self.model.insert_many(docs)

    # 6. Cập nhật theo ID
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

    # 7. Cập nhật nhiều document theo điều kiện
    async def update_many(self, conditions: dict[str, Any], update_data: dict[str, Any]) -> int:
        result = await self.model.find(conditions).update({"$set": update_data})
        return result.modified_count

    # 8. Xóa theo ID
    async def delete(self, id: Any) -> bool:
        db_item = await self.model.get(id)
        if not db_item:
            return False
        await db_item.delete()
        return True

    # 9. Xóa nhiều theo điều kiện
    async def delete_many(self, conditions: dict[str, Any]) -> int:
        result = await self.model.find(conditions).delete()
        return result.deleted_count

    # 10. Đếm số lượng document theo điều kiện
    async def count(self, conditions: dict[str, Any] | None = None) -> int:
        conditions = conditions or {}
        return await self.model.find(conditions).count()
