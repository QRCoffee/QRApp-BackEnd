from beanie import PydanticObjectId
from fastapi import APIRouter,Depends,Request
from app.api.dependency import login_required,required_role
from app.service import branchService,businessService
from typing import List
from app.common.http_exception import HTTP_404_NOT_FOUND,HTTP_403_FORBIDDEN,HTTP_400_BAD_REQUEST
from app.common.api_response import Response
from app.schema.branch import BranchResponse,BranchCreateWithoutBusiness
apiRouter = APIRouter(
    tags = ['Branch'],
    prefix = "/branchs",
    dependencies = [
        Depends(login_required),
        Depends(required_role(role=[
                'BusinessOwner'
            ])
        ),
    ]
)

@apiRouter.get(
    path = "",
    status_code=200,
    name = "Danh sách chi nhánh (Thuộc quyền sở hữu)",
    response_model=Response[List[BranchResponse]],
)
async def get_branchs(request:Request):
    business_id = request.state.user_scope
    branches = await branchService.find_many(conditions={
        "business.$id": PydanticObjectId(business_id)
    })
    return Response(data=branches)

@apiRouter.post(
    path = "",
    status_code=201,
    name = "Thêm chi nhánh cho doanh nghiệp",
    response_model=Response[BranchResponse],
)
async def post_branch(data:BranchCreateWithoutBusiness, request:Request):
    business = await businessService.find(request.state.user_scope)
    if data.contact is None:
        data.contact = business.contact
    data = data.model_dump()
    data['business'] = business
    branch = await branchService.insert(data)
    return Response(data=branch)

@apiRouter.delete(
    path = "/{id}",
    status_code=204,
    name = "Xóa chi nhánh",
)
async def delete_branch(id:PydanticObjectId, request:Request):
    branch = await branchService.find(id)
    if branch is None:
        raise HTTP_404_NOT_FOUND("Không tìm thấy")
    branch_scope = branch.business.to_ref().id
    user_scope = PydanticObjectId(request.state.user_scope)
    if branch_scope != user_scope:
        raise HTTP_403_FORBIDDEN("Bạn không đủ quyền thực hiện hành động này")
    if not await branchService.delete(id):
        raise HTTP_400_BAD_REQUEST("Lỗi")
    return True