from pydantic import BaseModel


class SignUp(BaseModel):
    username: str
    password: str

class SignIn(BaseModel):
    username: str
    password: str

class SignOut(BaseModel):
    refresh_token: str

class UserCreate(BaseModel):
    pass
class UserUpdate(BaseModel):
    pass