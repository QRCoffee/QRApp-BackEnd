from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Request

from app.api.dependency import login_required, required_role
from app.common.api_response import Response
from app.common.http_exception import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from app.schema.category import (CategoryCreate, CategoryResponse,
                                 SubCategoryCreate, SubCategoryResponse)
from app.service import businessService, categoryService, subcategoryService

apiRouter = APIRouter(
    tags = ["Category"],
    prefix = "/categories",
    dependencies = [
        Depends(login_required),
        Depends(required_role(
            "BusinessOwner",
        ))
    ]
)

@apiRouter.post(
    path = "",
    name = "Phân loại sản phẩm",
    status_code = 201,
    response_model=Response[CategoryResponse]
)
async def post_category(data:CategoryCreate,request:Request):
    business = await businessService.find(request.state.user_scope)
    if await categoryService.find_one(conditions={
        "name":data.name,
        "business.$id":business.id
        }
    ):
        raise HTTP_409_CONFLICT(f"Phân loại {data.name} đã tồn tại")
    data = data.model_dump()
    data['business'] = business
    category = await categoryService.insert(data)
    return Response(data=category)

@apiRouter.get(
    path = "",
    name = "Xem tất cả phân loại",
    status_code = 200,
    response_model=Response[List[CategoryResponse]]
)
async def post_category(request:Request):
    categories = await categoryService.find_many(conditions={
        "business.$id":PydanticObjectId(request.state.user_scope)
    })
    return Response(data=categories)

@apiRouter.get(
    path = "/{id}",
    name = "Xem một phân loại",
    status_code = 200,
    response_model=Response
)
async def view_category(id:PydanticObjectId,request:Request):
    category = await categoryService.find_one(conditions={
        "_id":id,
        "business.$id":PydanticObjectId(request.state.user_scope)
        },
        projection_model=CategoryResponse,
    )
    if category is None:
        raise HTTP_404_NOT_FOUND("Không tìm thấy phân loại")
    sub_categories = await subcategoryService.find_many(
        {"category._id":PydanticObjectId(category.id)},
        fetch_links = True,
        projection_model=SubCategoryResponse,
    )
    return Response(data=(category,sub_categories))

@apiRouter.post(
    path = "/{id}/subcategory",
    name = "Phân loại chi tiết",
    status_code = 201,
    response_model=Response
)
async def post_subcategory(id:PydanticObjectId,data:SubCategoryCreate,request:Request):
    category = await categoryService.find_one(conditions={
        "_id":id,
        "business.$id":PydanticObjectId(request.state.user_scope)
    })
    if category is None:
        raise HTTP_404_NOT_FOUND("Không tìm thấy phân loại")
    data = data.model_dump()
    data['category'] = category
    sub_category = await subcategoryService.insert(data)
    return Response(data=sub_category)