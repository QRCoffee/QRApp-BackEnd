from fastapi import APIRouter,Depends,Request
from beanie import PydanticObjectId
from typing import List,Any
from app.api.dependency import login_required
from app.service import orderService,productService
from app.common.api_response import Response
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
async def get_orders(request: Request):
    # Get orders
    orders = await orderService.find_many(conditions={
        "business.$id": PydanticObjectId(request.state.user_scope),
        "branch.$id": PydanticObjectId(request.state.user_branch),
    })
    for order in orders:
        for item in order.items:
            product = await productService.find(item.get('product').id)
            item['product'] = product
        pass
    return Response(data=orders)