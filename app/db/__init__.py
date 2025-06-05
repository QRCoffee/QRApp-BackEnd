from typing import Generator, List
from app.core.config import settings
from sqlalchemy.sql.schema import Table
from sqlmodel import Session, SQLModel, create_engine


class Database:
    def __init__(
        self,
        url:str,
    ):
        self.engine = create_engine(url)

    def create_session(self) -> Session:
        return Session(self.engine)
    
    def get_db(self) -> Generator[Session, None, None]:
        db = self.create_session()
        try:
            yield db
        finally:
            db.close()

    def initiate(self,tables:List[Table] = []) -> None:
        SQLModel.metadata.create_all(
            bind=self.engine,
            tables=tables,
        )

MySQL = Database(str(settings.MYSQL_DATABASE_URI))