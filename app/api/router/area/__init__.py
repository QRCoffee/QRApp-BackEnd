from fastapi import APIRouter, Depends, Request

from app.api.dependency import login_required, required_role
from app.schema.area import AreaCreate

apiRouter = APIRouter(
    tags=['Area'],
    prefix='/areas',
    dependencies = [
        Depends(login_required),
        Depends(required_role(role=[
            "BusinessOwner"
        ]))
    ]
)

@apiRouter.post(
    path = "",
    name = "Tạo khu vực"
)
def post_area(data:AreaCreate,request:Request):
    return data