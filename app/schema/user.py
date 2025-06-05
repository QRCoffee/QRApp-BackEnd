from pydantic import BaseModel

class SignUp(BaseModel):
    username: str
    password: str

class SignIn(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    password: str