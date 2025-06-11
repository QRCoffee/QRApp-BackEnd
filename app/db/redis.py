
import redis

from app.core.config import settings


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
        return True
    
Redis = RedisClient(
    host = settings.REDIS_HOST,
    port = settings.REDIS_PORT,
    db = settings.REDIS_DATABASE,
    username= settings.REDIS_USERNAME,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,
)