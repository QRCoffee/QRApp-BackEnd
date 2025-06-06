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
from app.core.security import ACCESS_JWT,REFRESH_JWT

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

@apiRouter.post(
    path = "/sign-in",
    name  = "Sign In",
    status_code=200,
)
def sign_in(data:SignIn,db: Session = Depends(MySQL.get_db)):
    user_service = UserService(db)
    user = user_service.find_by(
        by = "username",
        value = data.username,
    )
    if not user or not user.verify_password(data.password):
        raise UnauthorizedException("invalid credentials")
    return APIResponse(
        message="Login successful",
        data={
            "access_token":ACCESS_JWT.encode(user),
            "refresh_token":REFRESH_JWT.encode(user)
        }
    )
    
    