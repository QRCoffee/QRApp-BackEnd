from fastapi import APIRouter, Depends
from typing import List
from beanie import PydanticObjectId
from app.api.dependency import (login_required, required_permissions,
                                required_role)
from app.common.http_exception import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT,HTTP_404_NOT_FOUND
from app.common.api_response import Response
from app.schema.business import BusinessCreate,BusinessResponse
from app.schema.user import BusinessOwner, BusinessRegister,FullUserResponse
from app.service import businessService, businessTypeService, userService

apiRouter = APIRouter(
    tags=['Business'],
    prefix="/business",
    dependencies = [
        Depends(login_required),
        Depends(required_role(role=[
                'Admin'
            ])
        ),
    ]
)

@apiRouter.get(
    path = "",
    name = "Danh sách doanh nghiệp",
    status_code=200,
    dependencies = [Depends(
        required_permissions(permissions=[
            "view.business"
        ])
    )],
    response_model=Response[List[BusinessResponse]]
)
async def get_businesses():
    businesses = await businessService.find_many(fetch_links=True)
    return Response(data=businesses)

@apiRouter.post(
    path = "",
    name = "Đăng kí doanh nghiệp",
    status_code=201,
    dependencies = [Depends(
        required_permissions(permissions=[
            "create.business"
        ])
    )],
    response_model=Response[FullUserResponse]
)
async def post_business(data:BusinessRegister):
    type = await businessTypeService.find(data.business_type)
    if type is None:
        raise HTTP_400_BAD_REQUEST("Loại doanh nghiệp không phù hợp")
    if await businessService.find_one({"name":data.business_name}):
        raise HTTP_409_CONFLICT("Tên doanh nghiệp đã được đăng kí")
    if await userService.find_one({"username":data.username},):
        raise HTTP_409_CONFLICT("Tên người dùng đã được đăng kí")
    if await userService.find_one({"phone":data.owner_contact}):
        raise HTTP_409_CONFLICT("Số điện thoại người khác đã được sử dụng")
    if await businessService.find_one({"contact":data.business_contact}):
        raise HTTP_409_CONFLICT("Số điện thoại doanh nghiệp khác đăng kí")
    if data.business_tax_code:
        if await businessService.find_one({"tax_code":data.business_tax_code}):
            raise HTTP_409_CONFLICT("Mã số thuế đã được sử dụng")
    business = BusinessCreate(
        name = data.business_name,
        address=data.business_address,
        contact=data.business_contact,
        business_type=type,
        tax_code=data.business_tax_code,
        owner= None
    )
    owner = BusinessOwner(
        username = data.username,
        password = data.password,
        name = data.owner_name,
        phone= data.owner_contact,
        address=data.owner_address,
    )
    business = await businessService.insert(business)
    owner = await userService.insert(owner)
    await businessService.update(id = business.id,
        data = {
            "owner":owner,
        }
    )
    await userService.update(
        id = owner.id,
        data = {
            "business":business,
        }
    )
    user = await userService.find_one({"username":data.username})
    await user.fetch_all_links()
    return Response(data=user)

@apiRouter.post(
    path = "/{id}",
    name = "Mở/Khóa doanh nghiệp",
    dependencies = [Depends(
        required_permissions(permissions=[
            "update.business"
        ])
    )],
    response_model=Response[BusinessResponse]
)
async def lock_unlock_business(id:PydanticObjectId):
    business = await businessService.find(id)
    if business is None:
        raise HTTP_404_NOT_FOUND("Không tìm thấy doanh nghiệp")
    business = await businessService.update(id=id,data={"available": not business.available})
    await business.fetch_link('business_type')
    return Response(data=business)