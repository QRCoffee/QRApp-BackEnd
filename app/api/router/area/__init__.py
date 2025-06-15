from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, Query, Request

from app.common.exceptions import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from app.common.responses import APIResponse
from app.core.config import settings
from app.schema.area import AreaCreate, AreaResponse, AreaUpdate
from app.schema.table import TableCreate, TableResponse
from app.service import areaService, restaurantService, tableService

apiRouter = APIRouter(
    prefix="/areas",
)

@apiRouter.get(
    path = "",
    status_code=200,
    response_model=APIResponse[List[AreaResponse]],
)
async def get_areas(
    request:Request,
    page: int = Query(default=1,ge=1),
    limit: int = Query(default=settings.PAGE_SIZE, ge=1, le=50),
    name: Optional[str] = Query(default=None,description="Lọc theo tên"),
):
    restaurant_id = request.state.restaurant_id
    conditions={
        "restaurant._id": restaurant_id,
    }
    if name:
        conditions['name'] = {
            "$regex": name,
            "$options": "i"
        }
    areas = await areaService.find_many_by(
        conditions,
        skip=(page - 1) * limit,
        limit=limit,
    )
    return APIResponse(data=areas)

@apiRouter.get(
    path = "/{id}",
    status_code=200,
    response_model=APIResponse[AreaResponse],
)
async def get_area(
    id: PydanticObjectId,
    request:Request,
):
    area = await areaService.find_one_by(
        by = "_id",
        value = id
    )
    if area is None:
        raise HTTP_404_NOT_FOUND("Khu vực không tồn tại")
    if area.restaurant.id != request.state.restaurant_id:
        raise HTTP_403_FORBIDDEN("Khu vực này không thuộc quyền sở hữu của bạn")
    return APIResponse(data=area)

@apiRouter.put(
    path = "/{id}",
    status_code=200,
    # response_model=APIResponse[AreaResponse],
)
async def update_area(
    id: PydanticObjectId,
    data: AreaUpdate,
    request:Request,
):
    area = await areaService.find_one_by(
        by = "_id",
        value = id
    )
    if area is None:
        raise HTTP_404_NOT_FOUND("Khu vực không tồn tại")
    if area.restaurant.id != request.state.restaurant_id:
        raise HTTP_403_FORBIDDEN("Khu vực này không thuộc quyền sở hữu của bạn")
    area = await areaService.update(
        id = id,
        data = data
    )
    await area.fetch_all_links()
    return APIResponse(data=area)

@apiRouter.get(
    path = "/{id}/tables",
    status_code=200,
    response_model=APIResponse[List[TableResponse]],
)
async def get_tables_in_area(
    id: PydanticObjectId,
    request:Request,
):
    area = await areaService.find_one_by(
        by = "_id",
        value = id
    )
    if area is None:
        raise HTTP_404_NOT_FOUND("Khu vực không tồn tại")
    if area.restaurant.id != request.state.restaurant_id:
        raise HTTP_403_FORBIDDEN("Khu vực này không thuộc quyền sở hữu của bạn")
    conditions={
        "area._id": area.id,
    }
    tables = await tableService.find_many_by(conditions)
    return APIResponse(data=tables)

@apiRouter.post(
    path = "/{id}/tables",
    status_code=201,
    response_model=APIResponse[TableResponse],
)
async def add_table_in_area(
    id: PydanticObjectId,
    data: TableCreate,
    request:Request,
):
    area = await areaService.find_one_by(
        by = "_id",
        value = id
    )
    if area is None:
        raise HTTP_404_NOT_FOUND("Khu vực không tồn tại")
    if area.restaurant.id != request.state.restaurant_id:
        raise HTTP_403_FORBIDDEN("Khu vực này không thuộc quyền sở hữu của bạn")
    data = data.model_dump() 
    data['area'] = area
    table = await tableService.create(data)
    await table.fetch_all_links()
    return APIResponse(data=table)



@apiRouter.post(
    path = "",
    status_code = 201,
    response_model=APIResponse[AreaResponse]
)
async def add_area(data:AreaCreate,request:Request):
    restaurant_id = request.state.restaurant_id
    restaurant = await restaurantService.find_one_by(
        by = "_id",
        value = restaurant_id,
    )
    data = data.model_dump()
    data['restaurant'] = restaurant
    area = await areaService.create(data)
    return APIResponse(data=area)

@apiRouter.delete(
    path = "/{id}",
    status_code = 201,
    response_model=APIResponse[AreaResponse]
)
async def delete_area(id: PydanticObjectId,request:Request):
    area = await areaService.find_one_by(
        by = "_id",
        value = id
    )
    if area.restaurant.id != request.state.restaurant_id:
        raise HTTP_403_FORBIDDEN("Khu vực này không thuộc quyền sở hữu của bạn")
    await areaService.delete(area.id)
    return APIResponse(data=area)