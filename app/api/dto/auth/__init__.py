from pydantic import BaseModel


class SignUpDTO(BaseModel):
    username: str
    password: str
    role: str = "Staff"

class SignInDTO(BaseModel):
    username: str
    password: str

