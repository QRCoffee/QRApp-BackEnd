from sqlmodel import Session
from fastapi import APIRouter,Depends
from app.db import MySQL
from app.api.dependency import login_required
from app.common.responses import CreatedResponse,SuccessResponse
from app.common.exceptions import ConflictException,UnauthorizedException
from app.schema.user import SignUp,SignIn
from app.service import UserService

apiRouter = APIRouter(
    tags = ["Auth"],
)

@apiRouter.post(
    path = "/sign-up",
    name  = "Sign Up",
    status_code=201,
    dependencies=[
        Depends(login_required)
    ]
)
def sign_up(data:SignUp,db: Session = Depends(MySQL.get_db)):
    user_table = UserService(db)
    if user_table.find_by(
        by = "username",
        value = data.username,
    ):
        raise ConflictException(
            error="username has been used"
        )
    return CreatedResponse(
        data = user_table.create(data)
    )

@apiRouter.post(
    path = "/sign-in",
    name  = "Sign In",
    status_code=200,
)
def sign_in(data:SignIn,db: Session = Depends(MySQL.get_db)):
    user_table = UserService(db)
    user = user_table.find_by(
        by = "username",
        value = data.username,
    )
    if not user or user._password != data.password:
        raise UnauthorizedException(
            error = "Invalid Credentials"
        )
    return SuccessResponse(
        data = {
            "access_token":"123",
            "refresh_token":"456",
        }
    )
    
        