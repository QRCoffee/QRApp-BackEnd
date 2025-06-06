import redis
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

class RedisClient:
    def __init__(self,host:str,port:int,db:int,username:str,password:str,**kwargs):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            username=username,
            password=password,
            **kwargs,
        )
    def set(self,key,value,ttl) -> bool:
        self.client.set(
            name = key,
            value = value,
            ex = ttl,
        )
MySQL = Database(str(settings.MYSQL_DATABASE_URI))
Redis = RedisClient(
    host = settings.REDIS_HOST,
    port = settings.REDIS_PORT,
    db = settings.REDIS_DATABASE,
    username= settings.REDIS_USERNAME,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,
)