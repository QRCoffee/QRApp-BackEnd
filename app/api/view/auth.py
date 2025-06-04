from api.service import UserService
from db import mysql
from api.dependency import login_required
from api.dto.auth import SignInDTO,SignUpDTO
from fastapi import APIRouter, Depends
from api.view.response import (
    HTTP_200_OK,
    HTTP_409_CONFLICT
)

from sqlmodel import Session

apiRouter = APIRouter(
    tags = ["Auth"],
)
# Sign Up
@apiRouter.post(
    path="/sign-up",
    status_code=201,
    name="Sign Up",
    dependencies=[
        Depends(login_required)
    ]
)
def SignUp(
    data:SignUpDTO,
    db: Session = Depends(mysql.get_db),
):
    if UserService(db).find_by(
        by="username",
        value=data.username
    ):
        return HTTP_409_CONFLICT(
            error = "username has been used"
        )
    return HTTP_200_OK(
        data = UserService(db).create(data)
    )
# Sign In
@apiRouter.post(
    path="/sign-in",
    status_code=200,
    name="Sign In",
)
def SignIn(data:SignInDTO,db: Session = Depends(mysql.get_db)):
    if user := UserService(db).find_by(
        by="username",
        value=data.username
    ):
        if user.password == data.password:
            return True
        raise HTTPException(403,"Forbidden")
    raise HTTPException(403,"Forbidden")
# Sign Out
@apiRouter.post(
    path="/sign-out",
    status_code=200,
    name="Sign Out",
)
def SignOut(data:SignInDTO,db: Session = Depends(mysql.get_db)):
    if user := UserService(db).find_by(
        by="username",
        value=data.username
    ):
        if user.password == data.password:
            return True
        raise HTTPException(403,"Forbidden")
    raise HTTPException(403,"Forbidden")