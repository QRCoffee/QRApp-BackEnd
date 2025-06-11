
import redis

from app.core.config import settings


class RedisClient:
    def __init__(self,url,**kwargs):
        self.client = redis.Redis.from_url(url,**kwargs)
    def set(self,key,value,ttl) -> bool:
        self.client.set(
            name = key,
            value = value,
            ex = ttl,
        )
        return True
    def get(self,key):
        return self.client.get(key)
    def delete(self,key):
        self.client.delete(key)
        
Redis = RedisClient(settings.REDIS_URL,decode_responses=True)