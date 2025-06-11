import datetime

import jwt
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.core.config import settings
from app.db.redis import Redis


class JWTSecurity:
    def __init__(self,secret_key:str,algorithm:str = "HS256",expires_delta:datetime.timedelta | None = None):
        self.algorithm = algorithm
        self.expires_delta = expires_delta
        self.secret_key = secret_key
    def encode(self,payload: dict | BaseModel,session:bool = False) -> str:
        if isinstance(payload,dict):
            to_encode = payload.copy()
        else:
            to_encode = jsonable_encoder(payload)
        expire = datetime.datetime.now(datetime.timezone.utc) + (self.expires_delta if self.expires_delta else datetime.timedelta(minutes=15))
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        if session:
            Redis.set(
                key = to_encode.get("id"),
                value = token,
                ttl = int(self.expires_delta.total_seconds()),
            )
        return token
    def decode(self,token:str):
        return jwt.decode(token,self.secret_key,algorithms=[self.algorithm])

ACCESS_JWT = JWTSecurity(
    secret_key = settings.ACCESS_KEY,
    expires_delta=datetime.timedelta(minutes=1)
)
REFRESH_JWT = JWTSecurity(
    secret_key = settings.REFRESH_KEY,
    expires_delta=datetime.timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
)