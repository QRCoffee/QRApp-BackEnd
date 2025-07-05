import httpx
from fastapi import APIRouter, Depends, Request

from app.api.dependency import login_required, required_role
from app.common.api_response import Response
from app.core.decorator import limiter
from app.schema.payment import PaymentCreate, PaymentResponse
from app.service import paymentService, userService

apiRouter = APIRouter(
    tags=["Payment"],
    prefix="/payment",
    dependencies=[
        Depends(login_required),
        Depends(required_role(role=[
            "Admin",
            "BusinessOwner"
        ]))
    ],
)

@apiRouter.get(
    path = "/banks",
    name = "Danh sách ngân hàng",
    response_model=Response
)
@limiter(duration=120)
async def get_banks(request:Request):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.vietqr.io/v2/banks")
        data = response.json().get("data")
        return Response(data=data)
    

@apiRouter.post(
    path = "/banks",
    name = "Thêm tài khoản ngân hàng",
    response_model=Response[PaymentResponse]
)
async def post_banks(data:PaymentCreate,request:Request):
    user = await userService.find(request.state.user_id)
    data_dict = data.model_dump(by_alias=False) 
    data_dict['business'] = user.business.to_ref()
    payment = await paymentService.insert(data_dict)
    return Response(data=payment)