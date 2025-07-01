from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Query, Request

from app.api.dependency import login_required
from app.common.api_response import Response
from app.common.http_exception import (HTTP_400_BAD_REQUEST,
                                       HTTP_404_NOT_FOUND, HTTP_409_CONFLICT)
from app.schema.product import (FullProductResponse, ProductCreate,
                                ProductResponse, ProductUpdate)
from app.service import productService, subcategoryService

apiRouter = APIRouter(
    tags = ["Product"],
    prefix="/products",
    dependencies = [
        Depends(login_required),
    ],
)

@apiRouter.get(
    path = "",
    name = "Xem danh sách sản phẩm",
    status_code=200,
    response_model=Response[List[FullProductResponse]]
)
async def get_product(
    request:Request,
    category: Optional[PydanticObjectId] = Query(default=None),
    sub_category: Optional[PydanticObjectId] = Query(default=None),
):
    conditions={
        "business._id": PydanticObjectId(request.state.user_scope)
    }
    if category:
        conditions['category._id'] = category
    if sub_category:
        conditions['subcategory._id'] = sub_category
    products = await productService.find_many(
        conditions,
        fetch_links=True
    )
    return Response(data=products)

@apiRouter.post(
    path = "",
    name = "Sản phẩm",
    status_code=201,
    response_model=Response[ProductResponse]
)
async def post_product(data:ProductCreate,request:Request):
    subcategory = await subcategoryService.find(data.sub_category)
    if subcategory is None:
        raise HTTP_404_NOT_FOUND("Không tìm thấy phân loại")
    if product := await productService.find_one(conditions={
        "subcategory.$id":subcategory.id,
        "name": data.name
    }):
        raise HTTP_409_CONFLICT(f"Món {data.name} đã có trong Menu")
    await subcategory.fetch_link("category")
    category = subcategory.category
    business = category.business
    if business.id != PydanticObjectId(request.state.user_scope):
        raise HTTP_404_NOT_FOUND("Không tìm thấy phân loại")
    data = data.model_dump()
    data["category"] = category
    data["subcategory"] = subcategory
    data["business"] = business
    product = await productService.insert(data)
    return Response(data=product)

@apiRouter.put(
    path = "/{id}",
    name = "Sửa thông tin sản phẩm",
    status_code=201,
    response_model=Response[ProductResponse]
)
async def post_product(id:PydanticObjectId,data:ProductUpdate,request:Request):
    product = await productService.find(id)
    if product is None or product.business.to_ref().id != PydanticObjectId(request.state.user_scope):
        raise HTTP_404_NOT_FOUND("Không tìm thấy sản phẩm")
    product = await productService.update(id,data)
    return Response(data=product)

@apiRouter.delete(
    path = "/{id}",
    name = "Xóa sản phẩm",
    status_code=200,
    response_model=Response
)
async def post_product(id:PydanticObjectId,request:Request):
    product = await productService.find(id)
    if product is None or product.business.to_ref().id != PydanticObjectId(request.state.user_scope):
        raise HTTP_404_NOT_FOUND("Không tìm thấy sản phẩm")
    if not await productService.delete(id):
        raise HTTP_400_BAD_REQUEST("Xóa thất bại")
    return Response(data="Xóa thành công")
        