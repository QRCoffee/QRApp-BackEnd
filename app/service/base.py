from typing import Any, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel
from sqlmodel import Session, SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class Service(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType], db: Session):
        self.db = db
        self.model = model

    def find_by(
        self,
        by: str = "id",
        value: Any | None = None,
    ) -> Optional[ModelType]:
        query = select(self.model).where(getattr(self.model, by) == value)
        return self.db.exec(query).first()

    def find_all(self) -> List[ModelType]:
        query = select(self.model)
        return self.db.exec(query).all()

    def create(self, data: Union[dict, CreateSchemaType]) -> ModelType:
        if isinstance(data, BaseModel):
            data = data.model_dump()
        validated_data = self.model.model_validate(data)
        db_item = self.model(**validated_data.model_dump())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def update(self, id: int, data: Union[dict, UpdateSchemaType]) -> Optional[ModelType]:
        db_item = self.find_by(value=id)
        if not db_item:
            return None
        
        if isinstance(data, BaseModel):
            data = data.model_dump()

        for key, value in data.items():
            setattr(db_item, key, value)
        
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete(self, id: int) -> bool:
        db_item = self.find_by(value=id)
        if not db_item:
            return False
        
        self.db.delete(db_item)
        self.db.commit()
        return True