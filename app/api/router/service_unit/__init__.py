from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Query, Request

from app.api.dependency import login_required, required_role
from app.common.api_response import Response
from app.common.http_exception import HTTP_404_NOT_FOUND
from app.schema.service_unit import ServiceUnitCreate, ServiceUnitResponse
from app.service import areaService, unitService

apiRouter = APIRouter(
    tags = ['Service Unit'],
    prefix = "/services",
    dependencies = [
        Depends(login_required),
        Depends(required_role(role=[
            "BusinessOwner"
            ])
        ),
    ]
)

@apiRouter.get(
    path = "",
    name = "Xem đơn vị dịch vụ",
    response_model=Response[List[ServiceUnitResponse]],
)
async def post_service(
    request:Request,
    area: PydanticObjectId = Query(description="Lọc đơn vị theo khu vực")
):
    area = await areaService.find(area)
    if area is None:
        raise HTTP_404_NOT_FOUND("Không tìm thấy khu vực")
    if PydanticObjectId(request.state.user_scope) != area.business.to_ref().id:
        raise HTTP_404_NOT_FOUND("Không tìm thấy khu vực trong doanh nghiệp của bạn")
    conditions = {
        "area._id":area.id
    }
    services = await unitService.find_many(
        conditions,
        fetch_links=True
    )
    return Response(data=services)

@apiRouter.post(
    path = "",
    name = "Tạo đơn vị dịch vụ",
    response_model=Response[ServiceUnitResponse],
)
async def post_service(data:ServiceUnitCreate,request:Request):
    area = await areaService.find(data.area)
    if area is None:
        raise HTTP_404_NOT_FOUND("Không tìm thấy khu vực")
    if PydanticObjectId(request.state.user_scope) != area.business.to_ref().id:
        raise HTTP_404_NOT_FOUND("Không tìm thấy khu vực trong doanh nghiệp của bạn")
    data = await unitService.insert(data)
    await data.fetch_link('area')
    return Response(data=data)
    