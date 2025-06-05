from sqlmodel import Session
from fastapi import APIRouter,Depends
from app.db import MySQL
from app.models import User
from pydantic import BaseModel
from app.api.dependency import login_required
from app.common.responses import APIResponse
from app.common.exceptions import ConflictException,UnauthorizedException
from app.schema.user import SignUp,SignIn
from app.service import UserService

class TestResponse(BaseModel):
    message: str
    data:str = "123"
apiRouter = APIRouter(
    tags = ["Auth"],
)

@apiRouter.post(
    path = "/sign-up",
    name  = "Sign Up",
    status_code=201,
    response_model=APIResponse[User],
    response_model_exclude={
        "data": {
            "password",
        }
    },
    dependencies=[
        Depends(login_required)
    ],
)
def sign_up(data:SignUp,db: Session = Depends(MySQL.get_db)):
    user_service = UserService(db)
    if user_service.find_by(
        by = "username",
        value = data.username,
    ):
        raise ConflictException("username has been used")
    data = user_service.create(data)
    return APIResponse(
        message="registregister successfully",
        data=data,
    )