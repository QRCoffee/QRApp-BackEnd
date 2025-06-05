from sqlmodel import Session
from fastapi import APIRouter,Depends
from app.db import MySQL
from app.common.responses import CreatedResponse
from app.common.exceptions import NotFoundException
from app.schema.user import SignUp
from app.service import UserService
apiRouter = APIRouter(
    tags = ["Auth"],
)

@apiRouter.post(
    path = "/sign-up",
    name  = "Sign Up",
    status_code=201,
)
def register(data:SignUp,db: Session = Depends(MySQL.get_db)):
    UserTable = UserService(db)
    if UserTable.find_by(
        by = "username",
        value = data.username,
    ):
        raise NotFoundException({
            "message":"Conflict",
            "error":"username has been used"
        })
    return CreatedResponse(
        data = UserTable.create(data)
    )