from typing import Any, List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Query, Request

from app.api.dependency import login_required
from app.common.api_response import Response
from app.common.http_exception import HTTP_403_FORBIDDEN
from app.schema.order import OrderStatus, OrderUpdate
from app.service import orderService, productService

apiRouter = APIRouter(
    prefix = "/orders",
    tags = ["Order"],
    dependencies = [
        Depends(login_required),
    ]
)

@apiRouter.get(
    path = "",
    response_model=Response[List[Any]]
)
async def get_orders(
    request: Request,
    area: Optional[PydanticObjectId] = Query(default=None),
    service_unit: Optional[PydanticObjectId] = Query(default=None)
,):
    conditions={
        "business.$id": PydanticObjectId(request.state.user_scope),
        "branch.$id": PydanticObjectId(request.state.user_branch),
    }
    if area:
        conditions["area.$id"] = area
    if service_unit:
        conditions["service_unit.$id"] = service_unit
    orders = await orderService.find_many(conditions)
    for order in orders:
        for item in order.items:
            product = await productService.find(item.get('product').id)
            item['product'] = product
        pass
    return Response(data=orders)

@apiRouter.post(
    path = "/checkout/{id}",
    name = "Checkout order",
    response_model=Response
)
async def post_orders(id:PydanticObjectId,request: Request):
    order = await orderService.find(id)
    if order.business != PydanticObjectId(request.state.user_scope):
        raise HTTP_403_FORBIDDEN("Bạn không đủ quyền thực hiện hành động này")
    if order.branch != PydanticObjectId(request.state.user_branch):
        raise HTTP_403_FORBIDDEN("Bạn không đủ quyền thực hiện hành động này")
    order = await orderService.update(id,OrderUpdate(status=OrderStatus.PAID))
    return Response(data=order)