from typing import Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Query, Request

from app.api.dependency import login_required
from app.common.api_response import Response
from app.common.http_exception import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from app.schema.product import (Option, ProductCreate, ProductResponse,
                                ProductUpdate)
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
    response_model=Response
)
async def get_product(
    request:Request,
    category: Optional[PydanticObjectId] = Query(default=None),
    sub_category: Optional[PydanticObjectId] = Query(default=None),
):
    conditions={
        "business.$id": PydanticObjectId(request.state.user_scope)
    }
    if category:
        conditions['category.$id'] = category
    if sub_category:
        conditions['subcategory.$id'] = sub_category
    products = await productService.find_many(conditions)
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
    price = data.price
    data = data.model_dump(exclude={"price"})
    data["category"] = category
    data["subcategory"] = subcategory
    data["business"] = business
    data.get("variants",[]).append(
        Option(price = price)
    )
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

@apiRouter.post(
    path = "/{id}/variants",
    name = "Thêm biến thể cho sản phẩm",
    status_code=201,
    response_model=Response[ProductResponse]
)
async def post_product(id:PydanticObjectId,data:Option,request:Request):
    product = await productService.find(id)
    if product is None or product.business.to_ref().id != PydanticObjectId(request.state.user_scope):
        raise HTTP_404_NOT_FOUND("Không tìm thấy sản phẩm")
    if data.type in [variant.type for variant in product.variants]:
        raise HTTP_409_CONFLICT("Sản phẩm đã có biến thể này")
    product = await productService.update_one(
        id=id,
        conditions={
            "$addToSet": {
                "variants": {
                    "$each": [data]
                }
            }
        }
    )
    return Response(data=product)

@apiRouter.delete(
    path = "/{id}/variants",
    name = "Xóa biến thể cho sản phẩm",
    status_code=200,
    response_model=Response[ProductResponse]
)
async def post_product(id:PydanticObjectId,data:Option,request:Request):
    product = await productService.find(id)
    if product is None or product.business.to_ref().id != PydanticObjectId(request.state.user_scope):
        raise HTTP_404_NOT_FOUND("Không tìm thấy sản phẩm")
    if data.type not in [variant.type for variant in product.variants]:
        raise HTTP_404_NOT_FOUND("Sản phẩm không thấy biến thể này")
    product = await productService.update(
        id=id,
        data = {
            "variants": [opt for opt in product.variants if opt.type != data.type]
        }
    )
    return Response(data=product)

@apiRouter.post(
    path = "/{id}/options",
    name = "Thêm options cho sản phẩm",
    status_code=201,
    response_model=Response[ProductResponse]
)
async def post_product(id:PydanticObjectId,data:dict,request:Request):
    product = await productService.find(id)
    if product is None or product.business.to_ref().id != PydanticObjectId(request.state.user_scope):
        raise HTTP_404_NOT_FOUND("Không tìm thấy sản phẩm")
    product = await productService.update_one(
        id=id,
        conditions={
            "$addToSet": {
                "options": {
                    "$each": [data]
                }
            }
        }
    )
    return Response(data=product)

@apiRouter.delete(
    path = "/{id}/options",
    name = "Xóa options cho sản phẩm",
    status_code=201,
    response_model=Response[ProductResponse]
)
async def post_product(id:PydanticObjectId,data:dict,request:Request):
    product = await productService.find(id)
    if product is None or product.business.to_ref().id != PydanticObjectId(request.state.user_scope):
        raise HTTP_404_NOT_FOUND("Không tìm thấy sản phẩm")
    product = await productService.update_one(
        id=id,
        conditions={
            "$pull": {
                "options": data
            }
        }
    )
    return Response(data=product)