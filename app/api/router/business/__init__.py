from fastapi import APIRouter, Depends
from beanie import PydanticObjectId
from app.api.dependency import (login_required, required_permissions,
                                required_role)
from app.common.exceptions import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT,HTTP_404_NOT_FOUND
from app.common.responses import APIResponse
from app.schema.business import BusinessCreate
from app.schema.user import BusinessOwner, BusinessRegister
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

@apiRouter.post(
    path = "",
    name = "Đăng kí doanh nghiệp",
    dependencies = [Depends(
        required_permissions(permissions=[
            "create.business"
        ])
    )],
    response_model=APIResponse
)
async def post_business(data:BusinessRegister):
    type = await businessTypeService.find_one_by(value=data.business_type)
    if type is None:
        raise HTTP_400_BAD_REQUEST("Loại doanh nghiệp không phù hợp")
    if await businessService.find_one_by(
        by = "name",
        value = data.business_name,
    ):
        raise HTTP_409_CONFLICT("Tên doanh nghiệp đã được đăng kí")
    if await userService.find_one_by(
        by = "username",
        value = data.username,
    ):
        raise HTTP_409_CONFLICT("Tên người dùng đã được đăng kí")
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
    business = await businessService.create(business)
    owner = await userService.create(owner)
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
    user = await userService.find_one_by(
        by = "username",
        value = data.username,
    )
    await user.fetch_all_links()
    return APIResponse(data=user)

@apiRouter.post(
    path = "/{id}",
    name = "Mở/Khóa doanh nghiệp",
    dependencies = [Depends(
        required_permissions(permissions=[
            "update.business"
        ])
    )],
    response_model=APIResponse
)
async def lock_unlock_business(id:PydanticObjectId):
    business = await businessService.find_one_by(value = id)
    if business is None:
        raise HTTP_404_NOT_FOUND("Không tìm thấy doanh nghiệp")
    business = await businessService.update(id=id,data={"available": not business.available})
    return APIResponse(data=business)