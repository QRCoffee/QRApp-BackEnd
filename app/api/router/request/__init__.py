import json

from fastapi import APIRouter, Request

from app.common.api_response import Response
from app.common.http_exception import HTTP_400_BAD_REQUEST
from app.core.decorator import limiter
from app.schema.request import RequestCreate
from app.service import areaService, requestService, unitService
from app.socket import manager

apiRouter = APIRouter(
    tags = ['Request'],
    prefix = "/request"
)

@apiRouter.post(
    path = "",
    response_model = Response[str]
)
@limiter(max_request=10)
async def request(data:RequestCreate,request:Request):
    service_unit = await unitService.find_one(conditions={
        "_id":data.service_unit,
        "area.$id":data.area
    }) 
    if service_unit is None:
        raise HTTP_400_BAD_REQUEST("Yêu cầu không phù hợp")
    area = await areaService.find(service_unit.area.to_ref().id)
    data = data.model_dump()
    data['branch'] = area.branch.to_ref()
    data['business'] = area.business.to_ref()
    await requestService.insert(data)
    await manager.broadcast(
        message=json.dumps({
            "message":f"{data.get("type")} {data.get("reason")}",
            "data":data.get("data"),
        }),
        business=area.business.to_dict().get("id"),
        branch=area.branch.to_dict().get("id"),
        permission="receive.request",
    )
    return Response(data="Yêu cầu đang được xử lí")