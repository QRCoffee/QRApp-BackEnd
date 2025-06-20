from fastapi import APIRouter, Depends, Request

from app.api.dependency import login_required
from app.common.api_response import Response
from app.schema.area import AreaCreate
from app.service import areaService, businessService

apiRouter = APIRouter(
    tags=['Area'],
    prefix='/areas',
    dependencies = [
        Depends(login_required),
        # Depends(required_permissions(permissions=[
        #     "create.area"
        #     ])
        # )
    ]
)

@apiRouter.post(
    path = "",
    name = "Tạo khu vực",
    status_code=201,
    response_model=Response
)
async def post_area(data:AreaCreate,request:Request):
    business = await businessService.find(request.state.user_scope)
    data = data.model_dump()
    data['business'] = business
    area = await areaService.insert(data)
    return Response(data=area)