from pydantic import BaseModel
from typing import Optional
from app.common.enum import UserRole

class SignUp(BaseModel):
    username: str
    password: str
    role: str = UserRole.STAFF

class SignIn(BaseModel):
    username: str
    password: str

class SignOut(BaseModel):
    refresh_token: str

class Session(BaseModel):
    access_token: str
    refresh_token: str