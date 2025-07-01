from fastapi import APIRouter

from app.common.api_response import Response
from app.common.http_exception import HTTP_400_BAD_REQUEST
from app.schema.request import RequestCreate
from app.service import areaService, unitService
from app.socket import manager

apiRouter = APIRouter(
    tags = ['Request'],
    prefix = "/request"
)

@apiRouter.post(
    path = "",
    response_model = Response[bool]
)
async def request(data:RequestCreate):
    service_unit = await unitService.find_one(conditions={
        "_id":data.service_unit,
        "area.$id":data.area
    }) 
    if service_unit is None:
        raise HTTP_400_BAD_REQUEST("Yêu cầu không phù hợp")
    area = await areaService.find(service_unit.area.to_ref().id)
    await manager.broadcast(
        message=f"{data.type} {data.reason}",
        group=area.business.to_dict().get("id"),
        branch=area.branch.to_dict().get("id"),
    )
    return Response(data=True)